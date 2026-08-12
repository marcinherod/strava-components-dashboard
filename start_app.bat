@echo off
echo.
echo  Strava Dashboard - starting...
echo.

if not exist venv (
    echo  ERROR: Virtual environment not found.
    echo  Please run install.bat first.
    pause
    exit /b 1
)

echo  Server running at http://localhost:5050
echo  Press Ctrl+C to stop.
echo.
venv\Scripts\python.exe app.py
pause
