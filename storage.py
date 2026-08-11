"""
Prosty lokalny zapis danych w plikach JSON (bez bazy danych).

data/config.json      - client_id, client_secret, tokeny, dane zawodnika
data/activities.json  - lista pobranych aktywności
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
ACTIVITIES_FILE = os.path.join(DATA_DIR, "activities.json")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def get_config() -> dict:
    _ensure_data_dir()
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def update_config(**kwargs):
    config = get_config()
    config.update(kwargs)
    _ensure_data_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_activities() -> list:
    _ensure_data_dir()
    if not os.path.exists(ACTIVITIES_FILE):
        return []
    with open(ACTIVITIES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_activities(activities: list):
    _ensure_data_dir()
    with open(ACTIVITIES_FILE, "w", encoding="utf-8") as f:
        json.dump(activities, f, indent=2, ensure_ascii=False)
