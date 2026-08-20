@echo off
title Agentic AI Multi-Platform Social Studio
echo ============================================================
echo        STARTING AGENTIC AI MULTI-PLATFORM SOCIAL STUDIO
echo ============================================================
echo.
echo [1/3] Navigating to Studio Directory...
cd /d "%~dp0"

echo [2/3] Activating AI Virtual Environment...
call venv\Scripts\activate.bat

echo [3/3] Launching Web App in your Browser...
start http://localhost:8501
streamlit run app.py

pause
