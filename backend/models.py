from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from backend.crypto import encrypt_token, decrypt_token

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    password_changed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    social_accounts = relationship("SocialAccount", back_populates="user", cascade="all, delete-orphan")
    post_logs = relationship("PostLog", back_populates="user", cascade="all, delete-orphan")
    task_logs = relationship("TaskLog", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    media_files = relationship("MediaFile", back_populates="user", cascade="all, delete-orphan")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    session_token_hash = Column(String(64), unique=True, index=True, nullable=False)
    refresh_token_hash = Column(String(64), unique=True, index=True, nullable=True)
    device_info = Column(String(255), default="Unknown Device")
    ip_address = Column(String(50), default="")
    remember_me = Column(Boolean, default=False)
    is_revoked = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="sessions")


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    platform = Column(String(50), nullable=False) # 'instagram', 'facebook', 'linkedin', 'whatsapp', 'twitter'
    platform_account_id = Column(String(100), nullable=False)
    platform_account_name = Column(String(150), nullable=False)
    access_token = Column(Text, nullable=True) # Encrypted ciphertext at rest
    refresh_token = Column(Text, nullable=True) # Encrypted ciphertext at rest
    token_type = Column(String(50), default="Bearer")
    scopes = Column(String(255), default="")
    expires_at = Column(DateTime, nullable=True)
    status = Column(String(30), default="ACTIVE") # 'ACTIVE', 'EXPIRED', 'ACTION_REQUIRED'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="social_accounts")
    post_results = relationship("PlatformPostResult", back_populates="social_account")

    def get_decrypted_access_token(self) -> str:
        """Returns the decrypted plaintext access token."""
        return decrypt_token(self.access_token) or ""

    def set_encrypted_access_token(self, plaintext_token: str):
        """Encrypts and sets the access token using AES-256-GCM."""
        self.access_token = encrypt_token(plaintext_token)

    def get_decrypted_refresh_token(self) -> str:
        """Returns the decrypted plaintext refresh token."""
        return decrypt_token(self.refresh_token) or ""

    def set_encrypted_refresh_token(self, plaintext_token: str):
        """Encrypts and sets the refresh token using AES-256-GCM."""
        self.refresh_token = encrypt_token(plaintext_token)


class PostLog(Base):
    __tablename__ = "post_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(64), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    content = Column(Text, nullable=False)
    media_url = Column(Text, nullable=True)
    is_video = Column(Boolean, default=False)
    overall_status = Column(String(30), default="PROCESSING") # 'PROCESSING', 'SUCCESS', 'PARTIAL_SUCCESS', 'FAILED'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="post_logs")
    platform_results = relationship("PlatformPostResult", back_populates="post_log", cascade="all, delete-orphan")


class PlatformPostResult(Base):
    __tablename__ = "platform_post_results"

    id = Column(Integer, primary_key=True, index=True)
    post_log_id = Column(Integer, ForeignKey("post_logs.id"), index=True, nullable=False)
    account_id = Column(Integer, ForeignKey("social_accounts.id"), nullable=True)
    platform = Column(String(50), nullable=False)
    account_name = Column(String(150), nullable=False)
    status = Column(String(30), default="PROCESSING") # 'SUCCESS', 'FAILED', 'ACTION_REQUIRED'
    platform_post_id = Column(String(150), nullable=True)
    error_code = Column(String(50), nullable=True)
    error_message = Column(Text, nullable=True)
    attempt = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    post_log = relationship("PostLog", back_populates="platform_results")
    social_account = relationship("SocialAccount", back_populates="post_results")


class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    task = Column(Text, nullable=False)
    plan = Column(Text, nullable=True)
    tools_used = Column(Text, nullable=True)
    result = Column(Text, nullable=True)
    status = Column(String(50), default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="task_logs")


class PlatformSettings(Base):
    __tablename__ = "platform_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    watermark_name = Column(String(100), default="AI Creator")
    whatsapp_phone = Column(String(50), default="")
    instagram_connected = Column(String(20), default="Ready")
    facebook_connected = Column(String(20), default="Ready")
    linkedin_connected = Column(String(20), default="Ready")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    event_type = Column(String(50), index=True, nullable=False) # 'LOGIN_SUCCESS', 'LOGIN_FAILED', 'LOGOUT', 'LOGOUT_ALL', 'TOKEN_REFRESH', 'SOCIAL_CONNECTED', 'SOCIAL_DISCONNECTED', 'POST_PUBLISHED', 'ACCOUNT_DELETED'
    ip_address = Column(String(50), default="")
    user_agent = Column(String(255), default="")
    details = Column(Text, default="{}") # JSON metadata (NEVER raw secrets/tokens)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")


class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    filename = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    storage_path = Column(String(500), nullable=False)
    is_video = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="media_files")
