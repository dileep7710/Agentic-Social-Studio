from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    task = Column(Text, nullable=False)
    plan = Column(Text, nullable=True)
    tools_used = Column(Text, nullable=True)
    result = Column(Text, nullable=True)
    status = Column(String(50), default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)

class PlatformSettings(Base):
    __tablename__ = "platform_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    watermark_name = Column(String(100), default="AI Creator")
    whatsapp_phone = Column(String(50), default="")
    instagram_connected = Column(String(20), default="Ready")
    facebook_connected = Column(String(20), default="Ready")
    linkedin_connected = Column(String(20), default="Ready")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
