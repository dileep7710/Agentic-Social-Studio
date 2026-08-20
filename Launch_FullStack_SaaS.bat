@echo off
title Agentic AI Omni-Studio Full-Stack SaaS Launcher
echo ========================================================
echo   🌌 Agentic AI Omni-Studio (Full-Stack Edition)
echo   FastAPI Backend + React Vite Tailwind Dashboard
echo ========================================================
echo.
echo [1/2] Starting FastAPI Backend Server on http://127.0.0.1:8000...
start "" cmd /k ".\venv\Scripts\uvicorn.exe backend.server:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Opening Full-Stack Web Application in your default browser...
timeout /t 3 >nul
start http://127.0.0.1:8000

echo.
echo ========================================================
echo  ✨ Full-Stack Web Dashboard is LIVE!
echo  👉 Web App URL: http://127.0.0.1:8000
echo  👉 API Docs URL: http://127.0.0.1:8000/docs
echo ========================================================
pause
