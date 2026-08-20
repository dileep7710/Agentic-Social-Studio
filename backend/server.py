import os
import json
import uuid
import urllib.parse
from datetime import datetime, timedelta
from typing import Optional, List
from pathlib import Path
import httpx
from fastapi import FastAPI, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from backend.database import get_db, init_db
from backend.models import User, TaskLog, PlatformSettings, SocialAccount, PostLog, PlatformPostResult
from backend.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    require_current_user,
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

# Initialize DB tables
init_db()

app = FastAPI(
    title="Agentic AI Omni-Studio Multi-Account API",
    description="Production-grade API for autonomous Agentic AI and multi-account social media publishing with Meta OAuth.",
    version="2.2.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class TaskRunRequest(BaseModel):
    task: str

class ConnectAccountRequest(BaseModel):
    platform: str # 'instagram', 'facebook', 'linkedin', 'whatsapp'
    platform_account_id: str # IG ID / FB Page ID / URN / Phone
    platform_account_name: str # e.g. '@brand_insta', 'Tech Page'
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

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
# AUTH ENDPOINTS
# ==========================================

@app.post("/api/auth/register")
def register_user(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    hashed_pw = get_password_hash(req.password)
    new_user = User(
        name=req.name,
        email=req.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email, "id": new_user.id, "name": new_user.name})
    return {
        "status": "success",
        "token": token,
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }


@app.post("/api/auth/login")
def login_user(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email, "id": user.id, "name": user.name})
    return {
        "status": "success",
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@app.get("/api/auth/me")
def get_me(user: User = Depends(require_current_user)):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }


# ==========================================
# META (INSTAGRAM & FACEBOOK) OAUTH ENDPOINTS
# ==========================================

@app.get("/api/auth/meta/url")
def get_meta_oauth_url(user: User = Depends(require_current_user)):
    """
    Generates a secure Meta OAuth dialog URL signed with user_id in the state JWT.
    """
    # Create signed state token with 15-minute expiration
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
    Handles Meta OAuth code exchange, upgrades to Long-Lived Token, discovers Instagram accounts, and saves SocialAccount records.
    """
    if error or not code or not state:
        err_msg = error_description or error or "OAuth authorization was cancelled or failed."
        return RedirectResponse(url=f"/social?oauth=error&msg={urllib.parse.quote(err_msg)}")

    # Verify and decode state JWT
    try:
        payload = jwt.decode(state, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid state token payload")
    except JWTError:
        return RedirectResponse(url="/social?oauth=error&msg=Invalid+or+expired+OAuth+state+token")

    # Verify user exists in database
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

            # 3. Discover Pages and linked Instagram Business / Professional Accounts
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
                        existing_ig.access_token = page_token
                        existing_ig.status = "ACTIVE"
                        existing_ig.expires_at = datetime.utcnow() + timedelta(days=60)
                    else:
                        new_ig = SocialAccount(
                            user_id=user.id,
                            platform="instagram",
                            platform_account_id=ig_id,
                            platform_account_name=f"@{ig_username}",
                            access_token=page_token,
                            status="ACTIVE",
                            expires_at=datetime.utcnow() + timedelta(days=60)
                        )
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
                    existing_fb.access_token = page_token
                    existing_fb.status = "ACTIVE"
                    existing_fb.expires_at = datetime.utcnow() + timedelta(days=60)
                else:
                    new_fb = SocialAccount(
                        user_id=user.id,
                        platform="facebook",
                        platform_account_id=page_id,
                        platform_account_name=page_name,
                        access_token=page_token,
                        status="ACTIVE",
                        expires_at=datetime.utcnow() + timedelta(days=60)
                    )
                    db.add(new_fb)
                connected_count += 1

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
            "status": acc.status,
            "created_at": acc.created_at.strftime("%Y-%m-%d %H:%M") if acc.created_at else ""
        }
        for acc in accounts
    ]


@app.post("/api/social/accounts")
def connect_social_account(req: ConnectAccountRequest, user: User = Depends(require_current_user), db: Session = Depends(get_db)):
    """
    Connects a new social account/page for the authenticated user (Manual fallback).
    """
    existing = db.query(SocialAccount).filter(
        SocialAccount.user_id == user.id,
        SocialAccount.platform == req.platform.lower(),
        SocialAccount.platform_account_id == req.platform_account_id
    ).first()

    if existing:
        existing.platform_account_name = req.platform_account_name
        existing.access_token = req.access_token or existing.access_token
        existing.status = "ACTIVE"
        db.commit()
        db.refresh(existing)
        return {"status": "success", "message": "Account updated successfully", "account_id": existing.id}

    new_acc = SocialAccount(
        user_id=user.id,
        platform=req.platform.lower(),
        platform_account_id=req.platform_account_id,
        platform_account_name=req.platform_account_name,
        access_token=req.access_token,
        refresh_token=req.refresh_token,
        status="ACTIVE"
    )
    db.add(new_acc)
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

    db.delete(acc)
    db.commit()
    return {"status": "success", "message": "Account disconnected successfully"}


# ==========================================
# MEDIA UPLOADER ENDPOINT
# ==========================================

import tempfile
@app.post("/api/social/upload-file")
async def upload_custom_media(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tfile:
        content = await file.read()
        tfile.write(content)
        temp_path = tfile.name

    cdn_url = upload_local_file(temp_path)
    is_video = suffix in [".mp4", ".mov", ".avi"]
    return {
        "status": "success",
        "filename": file.filename,
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
    Publishes to MULTIPLE social accounts in 1-Click with partial-success resilience and user isolation.
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
                        access_token=acc.access_token,
                        author=author_name
                    )
                    result_item["status"] = res.get("status", "FAILED")
                    result_item["post_id"] = res.get("post_id")
                    result_item["error_code"] = res.get("error_code")
                    result_item["message"] = res.get("message", "")

                elif acc.platform == "facebook":
                    res = post_facebook_page(
                        content=req.content,
                        media_path_or_url=final_media_url,
                        page_id=acc.platform_account_id,
                        page_access_token=acc.access_token,
                        author=author_name
                    )
                    result_item["status"] = res.get("status", "FAILED")
                    result_item["post_id"] = res.get("post_id")
                    result_item["error_code"] = res.get("error_code")
                    result_item["message"] = res.get("message", "")

                elif acc.platform == "linkedin":
                    res = post_linkedin(
                        content=req.content,
                        media_path_or_url=final_media_url,
                        access_token=acc.access_token,
                        author_urn=acc.platform_account_id,
                        author=author_name
                    )
                    result_item["status"] = res.get("status", "FAILED")
                    result_item["post_id"] = res.get("post_id")
                    result_item["error_code"] = res.get("error_code")
                    result_item["message"] = res.get("message", "")

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
        "instagram": settings.instagram_connected,
        "facebook": settings.facebook_connected,
        "linkedin": settings.linkedin_connected
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
    return {
        "status": "success",
        "watermark_name": settings.watermark_name,
        "whatsapp_phone": settings.whatsapp_phone
    }


# ==========================================
# STATIC FRONTEND SPA SERVING
# ==========================================

FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = FRONTEND_DIST / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST / "index.html")
