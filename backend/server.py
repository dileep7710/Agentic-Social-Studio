import os
import json
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import get_db, init_db
from backend.models import User, TaskLog, PlatformSettings
from backend.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    require_current_user
)
from backend.agent_bridge import execute_agent_task
from social_tools import (
    create_nature_quote_image,
    upload_local_file,
    broadcast_all_platforms
)

# Initialize DB tables
init_db()

app = FastAPI(
    title="Agentic AI Omni-Studio API",
    description="Production-grade API wrapper around the existing Agentic AI engine.",
    version="2.0.0"
)

# Enable CORS for Vite frontend
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

class ProfileUpdateRequest(BaseModel):
    watermark_name: Optional[str] = None
    whatsapp_phone: Optional[str] = None

class PublishRequest(BaseModel):
    content: str
    whatsapp_phone: Optional[str] = None
    media_url: Optional[str] = None
    is_video: Optional[bool] = False


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
# AGENT EXECUTION ENDPOINT
# ==========================================

@app.post("/api/agent/run")
def run_agent(req: TaskRunRequest, user: Optional[User] = Depends(get_current_user), db: Session = Depends(get_db)):
    if not req.task.strip():
        raise HTTPException(status_code=400, detail="Task query cannot be empty.")

    # Execute existing Agentic AI pipeline
    execution_result = execute_agent_task(req.task)

    # Save to database TaskLog
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
# TASK HISTORY ENDPOINTS
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


@app.get("/api/tasks/{task_id}")
def get_task_detail(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task log not found")
    return {
        "id": task.id,
        "task": task.task,
        "plan": task.plan,
        "tools_used": task.tools_used.split(",") if task.tools_used else [],
        "result": task.result,
        "status": task.status,
        "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S") if task.created_at else ""
    }


# ==========================================
# SOCIAL MEDIA ENDPOINTS
# ==========================================

@app.get("/api/social/status")
def get_social_status():
    return {
        "instagram": "Connected (Stories & Feed)",
        "facebook": "Connected (Timeline Share)",
        "linkedin": "Connected (Professional Share)",
        "whatsapp": "Connected (1-Click Delivery)"
    }


from fastapi import UploadFile, File
import tempfile
from pathlib import Path

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


@app.post("/api/social/publish")
def direct_social_publish(req: PublishRequest):
    if req.media_url:
        final_media_url = req.media_url
        res = broadcast_all_platforms(content=req.content, whatsapp_phone=req.whatsapp_phone)
    else:
        img_path = create_nature_quote_image(req.content, author="AI Studio", is_story=True)
        final_media_url = upload_local_file(img_path)
        res = broadcast_all_platforms(content=req.content, whatsapp_phone=req.whatsapp_phone)

    return {
        "status": "success",
        "cdn_url": final_media_url,
        "is_video": req.is_video,
        "detail": res
    }


# ==========================================
# SETTINGS ENDPOINT
# ==========================================

@app.get("/api/settings")
def get_settings(user: Optional[User] = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = user.id if user else None
    settings = db.query(PlatformSettings).filter(PlatformSettings.user_id == user_id).first()
    if not settings:
        settings = PlatformSettings(user_id=user_id, watermark_name=user.name if user else "AI Creator")
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return {
        "watermark_name": settings.watermark_name,
        "whatsapp_phone": settings.whatsapp_phone,
        "ai_model": "Llama 3.2 (3B) Autonomous Planner",
        "memory_records": 10
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
    return {"status": "success", "message": "Settings updated successfully"}


# ==========================================
# STATIC FRONTEND SERVING (SPA)
# ==========================================
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="static_assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = FRONTEND_DIST / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST / "index.html")

