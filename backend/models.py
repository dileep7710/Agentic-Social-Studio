from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    social_accounts = relationship("SocialAccount", back_populates="user", cascade="all, delete-orphan")
    post_logs = relationship("PostLog", back_populates="user", cascade="all, delete-orphan")
    task_logs = relationship("TaskLog", back_populates="user", cascade="all, delete-orphan")


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    platform = Column(String(50), nullable=False) # 'instagram', 'facebook', 'linkedin', 'whatsapp'
    platform_account_id = Column(String(100), nullable=False) # IG Account ID / FB Page ID / LinkedIn URN / WhatsApp Phone
    platform_account_name = Column(String(150), nullable=False) # e.g. '@dileep_personal', 'Tech Updates Page'
    access_token = Column(Text, nullable=True) # Account specific token
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    status = Column(String(30), default="ACTIVE") # 'ACTIVE', 'EXPIRED', 'ACTION_REQUIRED'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="social_accounts")
    post_results = relationship("PlatformPostResult", back_populates="social_account")


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
