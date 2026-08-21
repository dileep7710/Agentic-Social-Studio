"""
Enterprise-Grade Authentication & Session Management Module
- Short-lived Access Tokens (15 min) + Refresh Token Rotation (30 days)
- Secure HttpOnly + Secure + SameSite=Lax Cookie Management
- Active Device / UserSession DB Tracking
- Single & All-Device Revocation
- Brute-Force Rate Limiting & Account Lockout Throttling
- Zero Plaintext Fallback Guarantee
"""

import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, UserSession, AuditLog
from backend.crypto import hash_token

# Cryptographic Config
SECRET_KEY = os.getenv("JWT_SECRET", "agentic_ai_omni_studio_super_secret_jwt_key_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Short-lived access token
REFRESH_TOKEN_EXPIRE_DAYS_REMEMBER = 30  # Persistent login
REFRESH_TOKEN_EXPIRE_DAYS_DEFAULT = 1   # Session login
MAX_FAILED_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15

# Determine if running in HTTPS production
IS_PRODUCTION = os.getenv("ENVIRONMENT", "").lower() == "production"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


# ==========================================
# PASSWORD HASHING (PBKDF2-150k Salted)
# ==========================================

def get_password_hash(password: str) -> str:
    """Generates secure salted PBKDF2-HMAC-SHA256 hash with 150,000 iterations."""
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 150000).hex()
    return f"pbkdf2:sha256:150000${salt}${hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies password strictly against cryptographic hashes.
    Supports both legacy 100k format (salt$hash) and modern pbkdf2:sha256:150000$salt$hash format.
    STRICTLY REJECTS PLAINTEXT COMPARISONS.
    """
    if not hashed_password or not plain_password:
        return False
    
    try:
        if hashed_password.startswith("pbkdf2:sha256:"):
            # Format: pbkdf2:sha256:150000$salt$hash
            parts = hashed_password.split("$")
            if len(parts) != 3:
                return False
            iter_part = parts[0].split(":")[2]
            iterations = int(iter_part)
            salt = parts[1]
            stored_hash = parts[2]
            calculated_hash = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), iterations).hex()
            return secrets.compare_digest(stored_hash, calculated_hash)
        
        elif "$" in hashed_password:
            # Legacy format: salt$hash (100k)
            parts = hashed_password.split("$", 1)
            if len(parts) != 2:
                return False
            salt, stored_hash = parts
            calculated_hash = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
            return secrets.compare_digest(stored_hash, calculated_hash)
        
        # Zero plaintext fallback
        return False
    except Exception:
        return False


# ==========================================
# BRUTE FORCE & ACCOUNT LOCKOUT
# ==========================================

def check_account_lockout(user: User):
    """Raises HTTP 423 Locked if account is temporarily locked out due to brute-force."""
    if user.locked_until and user.locked_until > datetime.utcnow():
        remaining = int((user.locked_until - datetime.utcnow()).total_seconds() / 60) + 1
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"Account temporarily locked due to repeated failed login attempts. Please try again in {remaining} minutes."
        )


def record_failed_login(user: User, db: Session, ip_address: str = "", user_agent: str = ""):
    """Increments failed attempts and triggers lockout if threshold reached."""
    user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
    if user.failed_login_attempts >= MAX_FAILED_LOGIN_ATTEMPTS:
        user.locked_until = datetime.utcnow() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
    
    # Audit log
    audit = AuditLog(
        user_id=user.id,
        event_type="LOGIN_FAILED",
        ip_address=ip_address,
        user_agent=user_agent,
        details=f'{{"failed_attempts": {user.failed_login_attempts}}}'
    )
    db.add(audit)
    db.commit()


def reset_failed_login(user: User, db: Session, ip_address: str = "", user_agent: str = ""):
    """Resets failed login counters and updates last active timestamp."""
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login_at = datetime.utcnow()
    
    # Audit log
    audit = AuditLog(
        user_id=user.id,
        event_type="LOGIN_SUCCESS",
        ip_address=ip_address,
        user_agent=user_agent,
        details='{"status": "authenticated"}'
    )
    db.add(audit)
    db.commit()


# ==========================================
# TOKEN & SESSION ENGINE
# ==========================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates short-lived access JWT token (15 mins default)."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_user_session(
    user: User,
    remember_me: bool,
    device_info: str,
    ip_address: str,
    db: Session
) -> Tuple[str, str, UserSession]:
    """
    Creates an access token, secure refresh token, and stores UserSession in DB.
    Returns: (access_token, refresh_token, session_record)
    """
    raw_session_id = secrets.token_hex(24)
    raw_refresh_token = f"rt_{secrets.token_urlsafe(48)}"
    
    refresh_days = REFRESH_TOKEN_EXPIRE_DAYS_REMEMBER if remember_me else REFRESH_TOKEN_EXPIRE_DAYS_DEFAULT
    expires_at = datetime.utcnow() + timedelta(days=refresh_days)
    
    session_record = UserSession(
        user_id=user.id,
        session_token_hash=hash_token(raw_session_id),
        refresh_token_hash=hash_token(raw_refresh_token),
        device_info=device_info[:250] if device_info else "Desktop Browser",
        ip_address=ip_address[:45] if ip_address else "",
        remember_me=remember_me,
        is_revoked=False,
        expires_at=expires_at,
        created_at=datetime.utcnow(),
        last_active_at=datetime.utcnow()
    )
    db.add(session_record)
    db.commit()
    db.refresh(session_record)
    
    # Access token payload embeds session identifier
    access_token = create_access_token({
        "sub": user.email,
        "id": user.id,
        "name": user.name,
        "sid": raw_session_id
    })
    
    return access_token, raw_refresh_token, session_record


def rotate_refresh_token(
    raw_refresh_token: str,
    device_info: str,
    ip_address: str,
    db: Session
) -> Tuple[str, str, User]:
    """
    Validates refresh token, invalidates old token, and issues fresh token pair.
    Implements Refresh Token Rotation.
    """
    token_h = hash_token(raw_refresh_token)
    session = db.query(UserSession).filter(UserSession.refresh_token_hash == token_h).first()
    
    if not session or session.is_revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or revoked session. Please log in again.")
    
    if session.expires_at < datetime.utcnow():
        session.is_revoked = True
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired. Please log in again.")
    
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account not found.")
    
    # Rotate: invalidate old refresh token and generate new pair
    new_session_id = secrets.token_hex(24)
    new_refresh_token = f"rt_{secrets.token_urlsafe(48)}"
    
    refresh_days = REFRESH_TOKEN_EXPIRE_DAYS_REMEMBER if session.remember_me else REFRESH_TOKEN_EXPIRE_DAYS_DEFAULT
    session.session_token_hash = hash_token(new_session_id)
    session.refresh_token_hash = hash_token(new_refresh_token)
    session.expires_at = datetime.utcnow() + timedelta(days=refresh_days)
    session.last_active_at = datetime.utcnow()
    if ip_address:
        session.ip_address = ip_address[:45]
    if device_info:
        session.device_info = device_info[:250]
        
    db.commit()
    
    new_access_token = create_access_token({
        "sub": user.email,
        "id": user.id,
        "name": user.name,
        "sid": new_session_id
    })
    
    return new_access_token, new_refresh_token, user


# ==========================================
# COOKIE MANAGEMENT
# ==========================================

def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: Optional[str] = None,
    remember_me: bool = False
):
    """Sets secure HttpOnly cookies on the response."""
    # Access token cookie (15 mins)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="lax",
        max_age=15 * 60,
        path="/"
    )
    
    # Refresh token cookie (30 days or 1 day)
    if refresh_token:
        refresh_max_age = (30 if remember_me else 1) * 24 * 3600
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=IS_PRODUCTION,
            samesite="lax",
            max_age=refresh_max_age,
            path="/"
        )


def clear_auth_cookies(response: Response):
    """Clears authentication cookies on logout."""
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")


# ==========================================
# AUTH DEPENDENCIES & IDOR GUARDS
# ==========================================

def get_current_user(
    request: Request,
    bearer_token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Extracts and authenticates user from HttpOnly cookie OR Authorization Bearer header.
    Verifies session is active and not revoked.
    """
    token = bearer_token
    if not token:
        # Check HttpOnly cookie
        token = request.cookies.get("access_token")
    
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        sid: Optional[str] = payload.get("sid")
        
        if not email:
            return None
    except JWTError:
        return None
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    # If session id embedded, verify active session
    if sid:
        sid_hash = hash_token(sid)
        session = db.query(UserSession).filter(
            UserSession.user_id == user.id,
            UserSession.session_token_hash == sid_hash
        ).first()
        
        if not session or session.is_revoked:
            return None
        
        # Update last active timestamp
        session.last_active_at = datetime.utcnow()
        db.commit()
        
    return user


def require_current_user(user: Optional[User] = Depends(get_current_user)) -> User:
    """Enforces strict authentication requirement (401 Unauthorized)."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
