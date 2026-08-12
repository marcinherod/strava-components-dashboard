@echo off
:: Uruchamia aplikacje w tle przez Git Bash (dziala po zamknieciu okna)

:: Znajdz Git Bash
set GIT_BASH="C:\Program Files\Git\bin\bash.exe"
if not exist %GIT_BASH% set GIT_BASH="C:\Program Files (x86)\Git\bin\bash.exe"

if not exist %GIT_BASH% (
    echo BLAD: Nie znaleziono Git Bash.
    echo Zainstaluj Git for Windows ze strony https://git-scm.com/download/win
    pause
    exit /b 1
)

:: Uruchom start.sh w Git Bash w katalogu tego pliku .bat
%GIT_BASH% --login -c "cd '%~dp0' && ./start.sh"
pause
