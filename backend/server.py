import os
import json
import uuid
import tempfile
import urllib.parse
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple
from pathlib import Path
import httpx
from fastapi import FastAPI, Depends, HTTPException, status, Query, UploadFile, File, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from backend.database import get_db, init_db
from backend.models import (
    User,
    UserSession,
    SocialAccount,
    PostLog,
    PlatformPostResult,
    TaskLog,
    PlatformSettings,
    AuditLog,
    MediaFile
)
from backend.crypto import encrypt_token, decrypt_token, hash_token
from backend.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_user_session,
    rotate_refresh_token,
    set_auth_cookies,
    clear_auth_cookies,
    get_current_user,
    require_current_user,
    check_account_lockout,
    record_failed_login,
    reset_failed_login,
    SECRET_KEY,
    ALGORITHM
)
from backend.agent_bridge import execute_agent_task
from social_tools import (
    create_nature_quote_image,
    upload_local_file,
    resolve_media_url,
    post_instagram_feed,
    post_instagram_story,
    post_facebook_page,
    post_linkedin,
    post_whatsapp,
    broadcast_all_platforms
)

# Meta OAuth Configuration
META_APP_ID = os.getenv("META_APP_ID", os.getenv("FACEBOOK_APP_ID", "17841448994358440"))
META_APP_SECRET = os.getenv("META_APP_SECRET", os.getenv("FACEBOOK_APP_SECRET", ""))
META_REDIRECT_URI = os.getenv("META_REDIRECT_URI", "http://localhost:8000/api/auth/meta/callback")

# Initialize DB tables and migrations
init_db()

app = FastAPI(
    title="OneClick Post Secure Enterprise API",
    description="Production-grade API with AES-256-GCM token encryption, HttpOnly session cookies, refresh token rotation, and multi-platform publishing.",
    version="3.0.0"
)

# Allowed CORS Origins
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
]
custom_origin = os.getenv("FRONTEND_URL", "")
if custom_origin and custom_origin not in ALLOWED_ORIGINS:
    ALLOWED_ORIGINS.append(custom_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# SECURITY HEADERS MIDDLEWARE
# ==========================================

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' data: https: blob:; "
        "media-src 'self' https: blob:; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com;"
    )
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


# ==========================================
# IN-MEMORY RATE LIMITER (BRUTE FORCE DEFENSE)
# ==========================================

_FAILED_ATTEMPTS: Dict[str, List[datetime]] = {}

def check_ip_rate_limit(ip: str, max_attempts: int = 10, window_minutes: int = 15):
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=window_minutes)
    
    # Filter attempts within window
    if ip in _FAILED_ATTEMPTS:
        _FAILED_ATTEMPTS[ip] = [t for t in _FAILED_ATTEMPTS[ip] if t > window_start]
        if len(_FAILED_ATTEMPTS[ip]) >= max_attempts:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed requests. Please try again in 15 minutes."
            )
    else:
        _FAILED_ATTEMPTS[ip] = []

def record_ip_failure(ip: str):
    if ip:
        if ip not in _FAILED_ATTEMPTS:
            _FAILED_ATTEMPTS[ip] = []
        _FAILED_ATTEMPTS[ip].append(datetime.utcnow())


# ==========================================
# PYDANTIC SCHEMAS
# ==========================================

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str
    remember_me: Optional[bool] = False

class RefreshTokenRequest(BaseModel):
    refresh_token: Optional[str] = None

class TaskRunRequest(BaseModel):
    task: str

class ConnectAccountRequest(BaseModel):
    platform: str
    platform_account_id: str
    platform_account_name: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scopes: Optional[str] = None

class MultiAccountPublishRequest(BaseModel):
    content: str
    media_url: Optional[str] = None
    is_video: Optional[bool] = False
    account_ids: Optional[List[int]] = None
    whatsapp_phone: Optional[str] = None

class ProfileUpdateRequest(BaseModel):
    watermark_name: Optional[str] = None
    whatsapp_phone: Optional[str] = None


# ==========================================
# AUTH & SESSION ENDPOINTS
# ==========================================

@app.post("/api/auth/register")
def register_user(
    req: RegisterRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    ip_addr = request.client.host if request.client else ""
    user_agent = request.headers.get("User-Agent", "Unknown")
    
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")

    existing = db.query(User).filter(User.email == req.email.lower().strip()).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    hashed_pw = get_password_hash(req.password)
    new_user = User(
        name=req.name.strip(),
        email=req.email.lower().strip(),
        hashed_password=hashed_pw,
        failed_login_attempts=0,
        last_login_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create persistent session and issue cookie + token
    access_token, refresh_token, _ = create_user_session(
        user=new_user,
        remember_me=True,
        device_info=user_agent,
        ip_address=ip_addr,
        db=db
    )
    set_auth_cookies(response, access_token, refresh_token, remember_me=True)

    # Audit log
    audit = AuditLog(
        user_id=new_user.id,
        event_type="REGISTER_SUCCESS",
        ip_address=ip_addr,
        user_agent=user_agent,
        details='{"status": "account_created"}'
    )
    db.add(audit)
    db.commit()

    return {
        "status": "success",
        "token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }


@app.post("/api/auth/login")
def login_user(
    req: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    ip_addr = request.client.host if request.client else ""
    user_agent = request.headers.get("User-Agent", "Unknown")
    
    # Check IP-level rate limiting
    check_ip_rate_limit(ip_addr)

    email_clean = req.email.lower().strip()
    user = db.query(User).filter(User.email == email_clean).first()

    if not user:
        record_ip_failure(ip_addr)
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # Check account lockout
    check_account_lockout(user)

    # Verify password hash
    if not verify_password(req.password, user.hashed_password):
        record_ip_failure(ip_addr)
        record_failed_login(user, db, ip_address=ip_addr, user_agent=user_agent)
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # Success: reset lockout counters
    reset_failed_login(user, db, ip_address=ip_addr, user_agent=user_agent)

    # Create active session record & rotate tokens
    access_token, refresh_token, _ = create_user_session(
        user=user,
        remember_me=req.remember_me or False,
        device_info=user_agent,
        ip_address=ip_addr,
        db=db
    )
    set_auth_cookies(response, access_token, refresh_token, remember_me=req.remember_me or False)

    return {
        "status": "success",
        "token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@app.post("/api/auth/refresh")
def refresh_session(
    request: Request,
    response: Response,
    req: Optional[RefreshTokenRequest] = None,
    db: Session = Depends(get_db)
):
    """
    Transparently rotates refresh token and issues fresh access token.
    Reads refresh token from HttpOnly cookie or request body.
    """
    raw_refresh = None
    if req and req.refresh_token:
        raw_refresh = req.refresh_token
    elif request.cookies.get("refresh_token"):
        raw_refresh = request.cookies.get("refresh_token")

    if not raw_refresh:
        raise HTTPException(status_code=401, detail="No refresh token provided.")

    ip_addr = request.client.host if request.client else ""
    user_agent = request.headers.get("User-Agent", "Unknown")

    new_access_token, new_refresh_token, user = rotate_refresh_token(
        raw_refresh_token=raw_refresh,
        device_info=user_agent,
        ip_address=ip_addr,
        db=db
    )

    set_auth_cookies(response, new_access_token, new_refresh_token, remember_me=True)

    # Audit log
    audit = AuditLog(
        user_id=user.id,
        event_type="TOKEN_REFRESH",
        ip_address=ip_addr,
        user_agent=user_agent,
        details='{"status": "session_rotated"}'
    )
    db.add(audit)
    db.commit()

    return {
        "status": "success",
        "token": new_access_token,
        "refresh_token": new_refresh_token
    }


@app.post("/api/auth/logout")
def logout_user(
    request: Request,
    response: Response,
    user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logs out the user from the current device session and clears HttpOnly cookies.
    """
    if user:
        token = request.cookies.get("access_token")
        if not token:
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]

        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                sid = payload.get("sid")
                if sid:
                    sid_h = hash_token(sid)
                    session = db.query(UserSession).filter(
                        UserSession.user_id == user.id,
                        UserSession.session_token_hash == sid_h
                    ).first()
                    if session:
                        session.is_revoked = True
                        db.commit()
            except Exception:
                pass

        audit = AuditLog(
            user_id=user.id,
            event_type="LOGOUT",
            ip_address=request.client.host if request.client else "",
            user_agent=request.headers.get("User-Agent", ""),
            details='{"scope": "current_device"}'
        )
        db.add(audit)
        db.commit()

    clear_auth_cookies(response)
    return {"status": "success", "message": "Logged out successfully."}


@app.post("/api/auth/logout-all")
def logout_all_devices(
    request: Request,
    response: Response,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    """
    Revokes ALL active device sessions for the authenticated user.
    """
    sessions = db.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.is_revoked == False
    ).all()

    for s in sessions:
        s.is_revoked = True
    
    audit = AuditLog(
        user_id=user.id,
        event_type="LOGOUT_ALL",
        ip_address=request.client.host if request.client else "",
        user_agent=request.headers.get("User-Agent", ""),
        details=f'{{"revoked_sessions": {len(sessions)}}}'
    )
    db.add(audit)
    db.commit()

    clear_auth_cookies(response)
    return {"status": "success", "message": f"Successfully logged out of {len(sessions)} active devices."}


@app.get("/api/auth/sessions")
def list_active_sessions(
    request: Request,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns list of all active/recent device sessions for the user.
    """
    # Extract current session identifier
    current_sid_hash = None
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            sid = payload.get("sid")
            if sid:
                current_sid_hash = hash_token(sid)
        except Exception:
            pass

    sessions = db.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.is_revoked == False,
        UserSession.expires_at > datetime.utcnow()
    ).order_by(UserSession.last_active_at.desc()).all()

    return [
        {
            "id": s.id,
            "device_info": s.device_info,
            "ip_address": s.ip_address,
            "remember_me": s.remember_me,
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
            "last_active": s.last_active_at.strftime("%Y-%m-%d %H:%M") if s.last_active_at else "",
            "is_current": (s.session_token_hash == current_sid_hash)
        }
        for s in sessions
    ]


@app.delete("/api/auth/sessions/{session_id}")
def revoke_specific_session(
    session_id: int,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    """
    Revokes a specific device session with strict IDOR ownership check.
    """
    session = db.query(UserSession).filter(
        UserSession.id == session_id,
        UserSession.user_id == user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Device session not found or unauthorized.")

    session.is_revoked = True
    db.commit()
    return {"status": "success", "message": "Device session revoked successfully."}


@app.get("/api/auth/me")
def get_me(user: User = Depends(require_current_user)):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "last_login_at": user.last_login_at.strftime("%Y-%m-%d %H:%M") if user.last_login_at else None
    }


# ==========================================
# ACCOUNT DELETION & AUDIT LOGS (GDPR COMPLIANT)
# ==========================================

@app.delete("/api/account/me")
def delete_my_account(
    request: Request,
    response: Response,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    """
    Permanently deletes user account, purging all encrypted tokens, sessions,
    media files, post logs, and personal data.
    """
    # 1. Log account deletion audit
    audit = AuditLog(
        user_id=None,
        event_type="ACCOUNT_DELETED",
        ip_address=request.client.host if request.client else "",
        user_agent=request.headers.get("User-Agent", ""),
        details=f'{{"deleted_user_email": "{user.email}"}}'
    )
    db.add(audit)

    # 2. Delete user (cascades to sessions, social_accounts, post_logs, media_files, task_logs)
    db.delete(user)
    db.commit()

    clear_auth_cookies(response)
    return {"status": "success", "message": "Your account and all associated data have been permanently deleted."}


@app.get("/api/audit-logs")
def get_user_audit_logs(
    limit: int = 20,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns security audit trail for the authenticated user without sensitive data leakage.
    """
    logs = db.query(AuditLog).filter(
        AuditLog.user_id == user.id
    ).order_by(AuditLog.id.desc()).limit(limit).all()

    return [
        {
            "id": l.id,
            "event_type": l.event_type,
            "ip_address": l.ip_address,
            "user_agent": l.user_agent,
            "timestamp": l.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for l in logs
    ]


# ==========================================
# META (INSTAGRAM & FACEBOOK) OAUTH ENDPOINTS
# ==========================================

@app.get("/api/auth/meta/url")
def get_meta_oauth_url(user: User = Depends(require_current_user)):
    """
    Generates a secure Meta OAuth dialog URL signed with user_id in the state JWT.
    """
    state_payload = {
        "user_id": user.id,
        "nonce": uuid.uuid4().hex,
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    state_token = jwt.encode(state_payload, SECRET_KEY, algorithm=ALGORITHM)

    scope = "instagram_basic,instagram_content_publish,pages_show_list,pages_read_engagement,business_management"
    auth_url = (
        f"https://www.facebook.com/v21.0/dialog/oauth"
        f"?client_id={META_APP_ID}"
        f"&redirect_uri={urllib.parse.quote(META_REDIRECT_URI)}"
        f"&scope={scope}"
        f"&response_type=code"
        f"&state={state_token}"
    )

    return {
        "status": "success",
        "auth_url": auth_url
    }


@app.get("/api/auth/meta/callback")
def meta_oauth_callback(
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    error_description: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Handles Meta OAuth code exchange, upgrades to Long-Lived Token,
    encrypts tokens with AES-256-GCM, and saves SocialAccount records.
    """
    if error or not code or not state:
        err_msg = error_description or error or "OAuth authorization was cancelled or failed."
        return RedirectResponse(url=f"/social?oauth=error&msg={urllib.parse.quote(err_msg)}")

    try:
        payload = jwt.decode(state, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid state token payload")
    except JWTError:
        return RedirectResponse(url="/social?oauth=error&msg=Invalid+or+expired+OAuth+state+token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return RedirectResponse(url="/social?oauth=error&msg=User+not+found")

    try:
        with httpx.Client(timeout=35.0) as client:
            # 1. Exchange code for Short-Lived User Token
            token_res = client.get(
                "https://graph.facebook.com/v21.0/oauth/access_token",
                params={
                    "client_id": META_APP_ID,
                    "client_secret": META_APP_SECRET,
                    "redirect_uri": META_REDIRECT_URI,
                    "code": code
                }
            )
            token_data = token_res.json()
            short_token = token_data.get("access_token")

            if not short_token:
                err_msg = token_data.get("error", {}).get("message", "Failed to retrieve access token from Meta")
                return RedirectResponse(url=f"/social?oauth=error&msg={urllib.parse.quote(err_msg)}")

            # 2. Upgrade to 60-Day Long-Lived User Token if App Secret is available
            long_token = short_token
            if META_APP_SECRET:
                try:
                    exchange_res = client.get(
                        "https://graph.facebook.com/v21.0/oauth/access_token",
                        params={
                            "grant_type": "fb_exchange_token",
                            "client_id": META_APP_ID,
                            "client_secret": META_APP_SECRET,
                            "fb_exchange_token": short_token
                        }
                    )
                    if exchange_res.status_code == 200:
                        long_token = exchange_res.json().get("access_token", short_token)
                except Exception:
                    pass

            # 3. Discover Pages and linked Instagram Accounts
            accounts_res = client.get(
                "https://graph.facebook.com/v21.0/me/accounts",
                params={
                    "fields": "id,name,access_token,instagram_business_account{id,username,profile_picture_url}",
                    "access_token": long_token
                }
            )
            accounts_data = accounts_res.json()
            pages = accounts_data.get("data", [])
            connected_count = 0

            for page in pages:
                page_token = page.get("access_token") or long_token
                page_id = str(page.get("id"))
                page_name = page.get("name", f"Facebook Page {page_id[-4:]}")

                # Save / update Instagram Account if linked
                ig_data = page.get("instagram_business_account")
                if ig_data and "id" in ig_data:
                    ig_id = str(ig_data["id"])
                    ig_username = ig_data.get("username", f"instagram_{ig_id[-4:]}")

                    existing_ig = db.query(SocialAccount).filter(
                        SocialAccount.user_id == user.id,
                        SocialAccount.platform == "instagram",
                        SocialAccount.platform_account_id == ig_id
                    ).first()

                    if existing_ig:
                        existing_ig.platform_account_name = f"@{ig_username}"
                        existing_ig.set_encrypted_access_token(page_token)
                        existing_ig.status = "ACTIVE"
                        existing_ig.expires_at = datetime.utcnow() + timedelta(days=60)
                    else:
                        new_ig = SocialAccount(
                            user_id=user.id,
                            platform="instagram",
                            platform_account_id=ig_id,
                            platform_account_name=f"@{ig_username}",
                            status="ACTIVE",
                            expires_at=datetime.utcnow() + timedelta(days=60)
                        )
                        new_ig.set_encrypted_access_token(page_token)
                        db.add(new_ig)
                    connected_count += 1

                # Save / update Facebook Page
                existing_fb = db.query(SocialAccount).filter(
                    SocialAccount.user_id == user.id,
                    SocialAccount.platform == "facebook",
                    SocialAccount.platform_account_id == page_id
                ).first()

                if existing_fb:
                    existing_fb.platform_account_name = page_name
                    existing_fb.set_encrypted_access_token(page_token)
                    existing_fb.status = "ACTIVE"
                    existing_fb.expires_at = datetime.utcnow() + timedelta(days=60)
                else:
                    new_fb = SocialAccount(
                        user_id=user.id,
                        platform="facebook",
                        platform_account_id=page_id,
                        platform_account_name=page_name,
                        status="ACTIVE",
                        expires_at=datetime.utcnow() + timedelta(days=60)
                    )
                    new_fb.set_encrypted_access_token(page_token)
                    db.add(new_fb)
                connected_count += 1

            # Audit log
            audit = AuditLog(
                user_id=user.id,
                event_type="SOCIAL_CONNECTED",
                details=f'{{"provider": "meta", "accounts_connected": {connected_count}}}'
            )
            db.add(audit)
            db.commit()

            return RedirectResponse(url=f"/social?oauth=success&connected={connected_count}")

    except Exception as ex:
        return RedirectResponse(url=f"/social?oauth=error&msg={urllib.parse.quote(str(ex))}")


# ==========================================
# SOCIAL ACCOUNT MANAGEMENT (MULTI-ACCOUNT)
# ==========================================

@app.get("/api/social/accounts")
def get_user_social_accounts(user: User = Depends(require_current_user), db: Session = Depends(get_db)):
    """
    Returns all social accounts belonging to the authenticated user (NEVER exposing sensitive tokens).
    """
    accounts = db.query(SocialAccount).filter(SocialAccount.user_id == user.id).all()
    return [
        {
            "id": acc.id,
            "platform": acc.platform,
            "platform_account_id": acc.platform_account_id,
            "platform_account_name": acc.platform_account_name,
            "scopes": acc.scopes,
            "status": acc.status,
            "expires_at": acc.expires_at.strftime("%Y-%m-%d %H:%M") if acc.expires_at else None,
            "created_at": acc.created_at.strftime("%Y-%m-%d %H:%M") if acc.created_at else ""
        }
        for acc in accounts
    ]


@app.post("/api/social/accounts")
def connect_social_account(req: ConnectAccountRequest, user: User = Depends(require_current_user), db: Session = Depends(get_db)):
    """
    Connects a new social account with AES-256-GCM token encryption at rest.
    """
    existing = db.query(SocialAccount).filter(
        SocialAccount.user_id == user.id,
        SocialAccount.platform == req.platform.lower(),
        SocialAccount.platform_account_id == req.platform_account_id
    ).first()

    if existing:
        existing.platform_account_name = req.platform_account_name
        if req.access_token:
            existing.set_encrypted_access_token(req.access_token)
        if req.refresh_token:
            existing.set_encrypted_refresh_token(req.refresh_token)
        existing.status = "ACTIVE"
        db.commit()
        db.refresh(existing)
        return {"status": "success", "message": "Account updated successfully", "account_id": existing.id}

    new_acc = SocialAccount(
        user_id=user.id,
        platform=req.platform.lower(),
        platform_account_id=req.platform_account_id,
        platform_account_name=req.platform_account_name,
        scopes=req.scopes or "",
        status="ACTIVE"
    )
    if req.access_token:
        new_acc.set_encrypted_access_token(req.access_token)
    if req.refresh_token:
        new_acc.set_encrypted_refresh_token(req.refresh_token)

    db.add(new_acc)
    
    # Audit log
    audit = AuditLog(
        user_id=user.id,
        event_type="SOCIAL_CONNECTED",
        details=f'{{"platform": "{req.platform.lower()}", "account_name": "{req.platform_account_name}"}}'
    )
    db.add(audit)
    db.commit()
    db.refresh(new_acc)

    return {
        "status": "success",
        "message": f"Connected {req.platform} account '{req.platform_account_name}' successfully",
        "account_id": new_acc.id
    }


@app.delete("/api/social/accounts/{account_id}")
def delete_social_account(account_id: int, user: User = Depends(require_current_user), db: Session = Depends(get_db)):
    """
    Disconnects a social account verifying strict user ownership.
    """
    acc = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Social account not found")

    if acc.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this account")

    platform_name = acc.platform
    acc_name = acc.platform_account_name
    db.delete(acc)

    audit = AuditLog(
        user_id=user.id,
        event_type="SOCIAL_DISCONNECTED",
        details=f'{{"platform": "{platform_name}", "account_name": "{acc_name}"}}'
    )
    db.add(audit)
    db.commit()
    return {"status": "success", "message": "Account disconnected successfully"}


# ==========================================
# MEDIA VALIDATION & UPLOAD ENGINE
# ==========================================

MAX_UPLOAD_SIZE = 25 * 1024 * 1024  # 25 MB

def validate_magic_bytes(header: bytes) -> Tuple[bool, str]:
    """
    Validates file magic bytes against allowed image and video formats.
    Returns: (is_valid, detected_mime)
    """
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return True, "image/png"
    if header.startswith(b"\xff\xd8\xff"):
        return True, "image/jpeg"
    if header.startswith(b"RIFF") and b"WEBP" in header[:16]:
        return True, "image/webp"
    if b"ftyp" in header[:20]:
        return True, "video/mp4"
    return False, "application/octet-stream"


@app.post("/api/social/upload-file")
async def upload_custom_media(
    file: UploadFile = File(...),
    user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Secure media uploader with magic byte validation and size limits.
    """
    content = await file.read()
    
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds maximum allowed size of 25MB.")
    
    is_valid, detected_mime = validate_magic_bytes(content[:64])
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail="Invalid or unrecognized media format. Only PNG, JPEG, WebP, and MP4 files are permitted."
        )

    suffix = Path(file.filename or "upload.png").suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tfile:
        tfile.write(content)
        temp_path = tfile.name

    cdn_url = upload_local_file(temp_path)
    is_video = "video" in detected_mime or suffix in [".mp4", ".mov", ".avi"]

    if user:
        media_rec = MediaFile(
            user_id=user.id,
            filename=file.filename or "media_upload",
            mime_type=detected_mime,
            file_size_bytes=len(content),
            storage_path=cdn_url or temp_path,
            is_video=is_video
        )
        db.add(media_rec)
        db.commit()

    return {
        "status": "success",
        "filename": file.filename,
        "mime_type": detected_mime,
        "media_url": cdn_url or temp_path,
        "is_video": is_video
    }


# ==========================================
# 1-CLICK MULTI-ACCOUNT PUBLISHING ENGINE
# ==========================================

@app.post("/api/social/publish")
def publish_multi_account(
    req: MultiAccountPublishRequest,
    user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Publishes to MULTIPLE social accounts in 1-Click with AES token decryption,
    partial-success resilience, and strict user isolation.
    """
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Content/caption cannot be empty.")

    job_id = f"job_{uuid.uuid4().hex[:12]}"
    user_id = user.id if user else None
    author_name = user.name if user else "AI Studio"

    # Prepare final media URL with UUID file isolation
    final_media_url = req.media_url
    if not final_media_url:
        generated_path = create_nature_quote_image(req.content, author=author_name, is_story=True)
        final_media_url = upload_local_file(generated_path) or generated_path

    # Fetch accounts to publish to
    accounts_to_publish = []
    if req.account_ids and user:
        user_accounts = db.query(SocialAccount).filter(
            SocialAccount.user_id == user.id,
            SocialAccount.id.in_(req.account_ids)
        ).all()

        if len(user_accounts) != len(req.account_ids):
            raise HTTPException(status_code=403, detail="Forbidden: Unauthorized account access detected")

        accounts_to_publish = user_accounts

    if not accounts_to_publish and user:
        accounts_to_publish = db.query(SocialAccount).filter(
            SocialAccount.user_id == user.id,
            SocialAccount.status == "ACTIVE"
        ).all()

    # Create PostLog record
    post_log = None
    if user:
        post_log = PostLog(
            job_id=job_id,
            user_id=user.id,
            content=req.content,
            media_url=final_media_url,
            is_video=req.is_video,
            overall_status="PROCESSING"
        )
        db.add(post_log)
        db.commit()
        db.refresh(post_log)

    platform_results = []
    success_count = 0
    failure_count = 0

    if accounts_to_publish:
        for acc in accounts_to_publish:
            decrypted_token = acc.get_decrypted_access_token()
            result_item = {
                "account_id": acc.id,
                "platform": acc.platform,
                "account_name": acc.platform_account_name,
                "status": "FAILED",
                "post_id": None,
                "error_code": None,
                "message": ""
            }

            try:
                if acc.platform == "instagram":
                    res = post_instagram_feed(
                        content=req.content,
                        media_path_or_url=final_media_url,
                        user_id=acc.platform_account_id,
                        access_token=decrypted_token,
                        author=author_name
                    )
                    result_item["status"] = res.get("status", "FAILED")
                    result_item["post_id"] = res.get("post_id")
                    result_item["error_code"] = res.get("error_code")
                    result_item["message"] = res.get("message", "")
                    if res.get("status") == "FAILED" and "OAuthException" in str(res.get("message")):
                        acc.status = "ACTION_REQUIRED"

                elif acc.platform == "facebook":
                    res = post_facebook_page(
                        content=req.content,
                        media_path_or_url=final_media_url,
                        page_id=acc.platform_account_id,
                        page_access_token=decrypted_token,
                        author=author_name
                    )
                    result_item["status"] = res.get("status", "FAILED")
                    result_item["post_id"] = res.get("post_id")
                    result_item["error_code"] = res.get("error_code")
                    result_item["message"] = res.get("message", "")
                    if res.get("status") == "FAILED" and "OAuthException" in str(res.get("message")):
                        acc.status = "ACTION_REQUIRED"

                elif acc.platform == "linkedin":
                    res = post_linkedin(
                        content=req.content,
                        media_path_or_url=final_media_url,
                        access_token=decrypted_token,
                        author_urn=acc.platform_account_id,
                        author=author_name
                    )
                    result_item["status"] = res.get("status", "FAILED")
                    result_item["post_id"] = res.get("post_id")
                    result_item["error_code"] = res.get("error_code")
                    result_item["message"] = res.get("message", "")
                    if res.get("status") == "FAILED" and "EXPIRED" in str(res.get("error_code")):
                        acc.status = "ACTION_REQUIRED"

                elif acc.platform == "whatsapp":
                    res = post_whatsapp(
                        content=req.content,
                        target=acc.platform_account_id or req.whatsapp_phone,
                        media_path_or_url=final_media_url,
                        author=author_name
                    )
                    result_item["status"] = res.get("status", "SUCCESS")
                    result_item["message"] = res.get("message", "")
                    result_item["action_url"] = res.get("action_url")

            except Exception as ex:
                result_item["status"] = "FAILED"
                result_item["error_code"] = "EXECUTION_EXCEPTION"
                result_item["message"] = str(ex)

            if result_item["status"] == "SUCCESS":
                success_count += 1
            else:
                failure_count += 1

            platform_results.append(result_item)

            if post_log:
                db_res = PlatformPostResult(
                    post_log_id=post_log.id,
                    account_id=acc.id,
                    platform=acc.platform,
                    account_name=acc.platform_account_name,
                    status=result_item["status"],
                    platform_post_id=result_item["post_id"],
                    error_code=result_item["error_code"],
                    error_message=result_item["message"]
                )
                db.add(db_res)

    else:
        wa_res = post_whatsapp(content=req.content, target=req.whatsapp_phone, media_path_or_url=final_media_url, author=author_name)
        platform_results = [
            {
                "account_id": None,
                "platform": "instagram",
                "account_name": "Instagram Direct",
                "status": "ACTION_REQUIRED",
                "action_url": "https://www.instagram.com/",
                "message": "Ready for Instagram Story & Feed upload."
            },
            {
                "account_id": None,
                "platform": "facebook",
                "account_name": "Facebook Timeline",
                "status": "ACTION_REQUIRED",
                "action_url": f"https://www.facebook.com/sharer/sharer.php?u={final_media_url}&quote={req.content}",
                "message": "1-Click Facebook Timeline post ready."
            },
            {
                "account_id": None,
                "platform": "linkedin",
                "account_name": "LinkedIn Feed",
                "status": "ACTION_REQUIRED",
                "action_url": f"https://www.linkedin.com/sharing/share-offsite/?url={final_media_url}",
                "message": "1-Click LinkedIn share ready."
            },
            {
                "account_id": None,
                "platform": "whatsapp",
                "account_name": "WhatsApp Direct",
                "status": "SUCCESS",
                "action_url": wa_res.get("action_url"),
                "message": wa_res.get("message")
            }
        ]
        success_count = len(platform_results)

    if failure_count == 0:
        overall_status = "SUCCESS"
    elif success_count > 0 and failure_count > 0:
        overall_status = "PARTIAL_SUCCESS"
    else:
        overall_status = "FAILED"

    if post_log:
        post_log.overall_status = overall_status
        db.commit()

    if user:
        audit = AuditLog(
            user_id=user.id,
            event_type="POST_PUBLISHED",
            details=f'{{"job_id": "{job_id}", "status": "{overall_status}", "total": {len(platform_results)}}}'
        )
        db.add(audit)
        db.commit()

    return {
        "job_id": job_id,
        "overall_status": overall_status,
        "media_url": final_media_url,
        "is_video": req.is_video,
        "total_accounts": len(platform_results),
        "success_count": success_count,
        "failure_count": failure_count,
        "platforms": platform_results
    }


# ==========================================
# POST HISTORY AUDIT ENDPOINTS
# ==========================================

@app.get("/api/social/history")
def get_social_history(user: User = Depends(require_current_user), db: Session = Depends(get_db)):
    """
    Returns full multi-account posting audit history for the authenticated user.
    """
    posts = db.query(PostLog).filter(PostLog.user_id == user.id).order_by(PostLog.id.desc()).limit(30).all()
    return [
        {
            "id": p.id,
            "job_id": p.job_id,
            "content": p.content,
            "media_url": p.media_url,
            "is_video": p.is_video,
            "overall_status": p.overall_status,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M"),
            "results": [
                {
                    "platform": r.platform,
                    "account_name": r.account_name,
                    "status": r.status,
                    "post_id": r.platform_post_id,
                    "error": r.error_message
                }
                for r in p.platform_results
            ]
        }
        for p in posts
    ]


# ==========================================
# AGENT EXECUTION ENDPOINT (PRESERVED)
# ==========================================

@app.post("/api/agent/run")
def run_agent(req: TaskRunRequest, user: Optional[User] = Depends(get_current_user), db: Session = Depends(get_db)):
    if not req.task.strip():
        raise HTTPException(status_code=400, detail="Task query cannot be empty.")

    execution_result = execute_agent_task(req.task)

    new_log = TaskLog(
        user_id=user.id if user else None,
        task=req.task,
        plan=execution_result.get("plan", ""),
        tools_used=",".join(execution_result.get("tools_used", [])),
        result=execution_result.get("result", ""),
        status="completed"
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    execution_result["task_id"] = new_log.id
    return execution_result


# ==========================================
# TASK LOGS & SETTINGS ENDPOINTS (PRESERVED)
# ==========================================

@app.get("/api/tasks")
def get_task_history(
    limit: int = 20,
    user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(TaskLog)
    if user:
        query = query.filter((TaskLog.user_id == user.id) | (TaskLog.user_id.is_(None)))
    tasks = query.order_by(TaskLog.id.desc()).limit(limit).all()

    return [
        {
            "id": t.id,
            "task": t.task,
            "plan": t.plan,
            "tools_used": t.tools_used.split(",") if t.tools_used else [],
            "result": t.result,
            "status": t.status,
            "created_at": t.created_at.strftime("%Y-%m-%d %H:%M") if t.created_at else ""
        }
        for t in tasks
    ]


@app.get("/api/settings")
def get_settings(user: Optional[User] = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = user.id if user else None
    settings = db.query(PlatformSettings).filter(PlatformSettings.user_id == user_id).first()
    if not settings:
        settings = PlatformSettings(
            user_id=user_id,
            watermark_name=user.name if user else "AI Creator",
            whatsapp_phone="",
            instagram_connected="Connected",
            facebook_connected="Connected",
            linkedin_connected="Connected"
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return {
        "watermark_name": settings.watermark_name,
        "whatsapp_phone": settings.whatsapp_phone,
        "instagram_connected": settings.instagram_connected,
        "facebook_connected": settings.facebook_connected,
        "linkedin_connected": settings.linkedin_connected
    }


@app.post("/api/settings")
def update_settings(req: ProfileUpdateRequest, user: Optional[User] = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = user.id if user else None
    settings = db.query(PlatformSettings).filter(PlatformSettings.user_id == user_id).first()
    if not settings:
        settings = PlatformSettings(user_id=user_id)
        db.add(settings)

    if req.watermark_name is not None:
        settings.watermark_name = req.watermark_name
    if req.whatsapp_phone is not None:
        settings.whatsapp_phone = req.whatsapp_phone

    db.commit()
    db.refresh(settings)
    return {"status": "success", "settings": {
        "watermark_name": settings.watermark_name,
        "whatsapp_phone": settings.whatsapp_phone
    }}


# ==========================================
# STATIC SPA ROUTING (PRESERVED)
# ==========================================

FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = FRONTEND_DIST / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST / "index.html")
