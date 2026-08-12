@echo off
echo.
echo  Strava Dashboard - instalacja
echo  ==============================
echo.

:: Sprawdz czy Python jest dostepny
python --version >nul 2>&1
if errorlevel 1 (
    echo  BLAD: Python nie jest zainstalowany lub nie jest w PATH.
    echo  Pobierz Python 3.10+ ze strony https://www.python.org/downloads/
    echo  Pamietaj zaznaczyc "Add python.exe to PATH" podczas instalacji.
    pause
    exit /b 1
)

echo  [1/3] Python znaleziony:
python --version
echo.

:: Utworz venv jesli nie istnieje
if exist venv (
    echo  [2/3] Srodowisko wirtualne juz istnieje, pomijam tworzenie.
) else (
    echo  [2/3] Tworzenie srodowiska wirtualnego...
    python -m venv venv
    if errorlevel 1 (
        echo  BLAD: Nie udalo sie utworzyc venv.
        pause
        exit /b 1
    )
)
echo.

:: Zainstaluj zaleznosci
echo  [3/3] Instalowanie zaleznosci (Flask, requests)...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo  BLAD: pip install nie powiodl sie.
    pause
    exit /b 1
)

echo.
echo  ==============================
echo  Instalacja zakonczona!
echo.
echo  Aby uruchomic aplikacje:
echo    1. Uruchom start_app.bat  (lub wpisz: python app.py)
echo    2. Otworz http://localhost:5050 w przegladarce
echo  ==============================
echo.
pause
