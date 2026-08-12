@echo off
echo.
echo  Strava Dashboard - installation
echo  =================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python is not installed or not in PATH.
    echo  Download Python 3.10+ from https://www.python.org/downloads/
    echo  Make sure to check "Add python.exe to PATH" during installation.
    pause
    exit /b 1
)

echo  [1/3] Python found:
python --version
echo.

:: Create venv if it doesn't exist
if exist venv (
    echo  [2/3] Virtual environment already exists, skipping.
) else (
    echo  [2/3] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo  ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
)
echo.

:: Install dependencies
echo  [3/3] Installing dependencies (Flask, requests)...
venv\Scripts\pip.exe install -r requirements.txt --quiet
if errorlevel 1 (
    echo  ERROR: pip install failed.
    pause
    exit /b 1
)

echo.
echo  =================================
echo  Installation complete!
echo.
echo  To run the app:
echo    1. Double-click start_app.bat
echo    2. Open http://localhost:5050 in your browser
echo  =================================
echo.
pause
