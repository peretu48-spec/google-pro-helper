@echo off
chcp 65001 >nul
title Google AI Pro (5 TB) Zero Cost 2-Year Automated Console - Setup and Launch
cd /d "%~dp0"
echo ======================================================================
echo   Checking and installing Python dependencies (fastapi, uvicorn, playwright)...
echo ======================================================================
python -m pip install -r requirements.txt
echo.
echo ======================================================================
echo   Starting Web Console (http://127.0.0.1:8765) ...
echo ======================================================================
start "" "http://127.0.0.1:8765"
python app.py
pause
