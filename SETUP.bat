@echo off
echo ========================================
echo   AI Voice Detection - Railway Setup
echo ========================================
echo.

REM Step 1: Check if model file exists
echo [1/5] Checking for model file...
if exist "models\voice_detector.pkl" (
    echo   FOUND: models\voice_detector.pkl
) else (
    echo   ERROR: Model file not found!
    echo.
    echo   Please copy your trained model:
    echo   FROM: C:\AI VOICE DETECTION\AI_Voice_API\models\voice_detector.pkl
    echo   TO:   %CD%\models\voice_detector.pkl
    echo.
    pause
    exit /b 1
)

REM Step 2: Check Git
echo.
echo [2/5] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo   ERROR: Git not installed!
    echo   Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo   Git is installed

REM Step 3: Initialize Git
echo.
echo [3/5] Initializing Git repository...
git init
git add .
git commit -m "Initial commit - AI Voice Detection API"

REM Step 4: Instructions
echo.
echo [4/5] Git repository created!
echo ========================================
echo.
echo NEXT STEPS:
echo.
echo 1. Create GitHub repository:
echo    https://github.com/new
echo    Name: ai-voice-detection
echo    Type: Public
echo    DO NOT initialize with README
echo.
echo 2. Connect and push:
echo    git remote add origin https://github.com/YOUR_USERNAME/ai-voice-detection.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Deploy on Railway:
echo    https://railway.app/
echo    New Project ^> Deploy from GitHub repo
echo    Select: ai-voice-detection
echo.
echo ========================================
echo.

REM Step 5: Open browser
echo [5/5] Opening setup pages...
start https://github.com/new
timeout /t 2 >nul
start https://railway.app/

echo.
echo Setup script complete!
echo Follow the instructions above to deploy.
echo.
pause
