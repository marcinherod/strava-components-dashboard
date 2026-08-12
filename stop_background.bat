@echo off
:: Zatrzymuje aplikacje dzialajaca w tle

set GIT_BASH="C:\Program Files\Git\bin\bash.exe"
if not exist %GIT_BASH% set GIT_BASH="C:\Program Files (x86)\Git\bin\bash.exe"

if not exist %GIT_BASH% (
    echo BLAD: Nie znaleziono Git Bash.
    pause
    exit /b 1
)

%GIT_BASH% --login -c "cd '%~dp0' && ./stop.sh"
pause
