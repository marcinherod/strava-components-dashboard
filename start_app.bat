@echo off
echo.
echo  Strava Dashboard - uruchamianie...
echo.

if not exist venv (
    echo  BLAD: Nie znaleziono srodowiska wirtualnego.
    echo  Uruchom najpierw install.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
echo  Serwer dziala na http://localhost:5050
echo  Nacisnij Ctrl+C zeby zatrzymac.
echo.
python app.py
pause
