# Strava Dashboard — jeden proces Python

Cała aplikacja (backend + interfejs) w jednym procesie Flask. Konfiguracja
(Client ID / Secret) odbywa się w przeglądarce, bez edytowania plików.

## 1. Instalacja

```powershell
cd strava-dashboard
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Uruchomienie

### Windows (PowerShell) — najprostszy sposób

```powershell
venv\Scripts\activate
python app.py
```

Aplikacja działa dopóki terminal jest otwarty (Ctrl+C żeby zatrzymać).

### Uruchomienie w tle (Git Bash) — opcjonalnie

Jeśli chcesz, żeby aplikacja działała dalej po zamknięciu terminala,
otwórz **Git Bash** w folderze projektu (prawy klik → "Git Bash Here") i użyj:

```bash
./start.sh   # uruchomienie w tle
./stop.sh    # zatrzymanie
tail -f app.log   # logi na bieżąco
```

## 3. Konfiguracja w przeglądarce

Otwórz **http://localhost:5050** — zostaniesz przekierowany do `/settings`.

1. Załóż własną aplikację na [strava.com/settings/api](https://www.strava.com/settings/api)
   ("Authorization Callback Domain" ustaw na `localhost`)
2. Wklej **Client ID** i **Client Secret** w formularzu, zapisz
3. Kliknij **"Autoryzuj przez Stravę"**, zaloguj się i zatwierdź dostęp
4. Na dashboardzie kliknij **"Synchronizuj ze Stravą"**, żeby pobrać aktywności

Kolejne synchronizacje pobierają tylko nowe aktywności (te już zapisane są pomijane).

## Struktura projektu

```
strava-dashboard/
├── app.py              # routing Flask, logika stron
├── storage.py          # zapis/odczyt danych w plikach JSON
├── strava_client.py    # OAuth2 + zapytania do Strava API
├── requirements.txt
├── start.sh / stop.sh   # uruchamianie w tle (Git Bash)
├── templates/
│   ├── base.html
│   ├── settings.html
│   └── dashboard.html
├── static/style.css
└── data/                # tworzone automatycznie
    ├── config.json      # Client ID/Secret + tokeny (NIE trafia do gita)
    └── activities.json  # zapisane aktywności (NIE trafia do gita)
```

## Uwaga o bezpieczeństwie

`data/config.json` zawiera Twój Client Secret i tokeny dostępu — jest w `.gitignore`,
więc nigdy nie trafi na GitHub. Nie udostępniaj tego pliku nikomu.

## Co dalej (pomysły na rozbudowę)

- Wykresy dystansu/tempa w czasie (np. Chart.js w dashboard.html)
- Filtrowanie aktywności po typie (bieganie, rower, itd.)
- Mapa tras (Strava zwraca zakodowaną polyline dla każdej aktywności)
- Prawdziwa baza danych (SQLite) zamiast plików JSON — lepsza przy dużej historii
