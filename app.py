"""
Strava Dashboard - jeden proces Flask, konfiguracja w przeglądarce.

Uruchomienie:
    python app.py
Otwórz: http://localhost:5050
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import time

import storage
import strava_client
import components_parser

app = Flask(__name__)


@app.route("/")
def dashboard():
    config = storage.get_config()

    if not config.get("client_id") or not config.get("client_secret"):
        return redirect(url_for("settings"))

    if not config.get("access_token"):
        # Skonfigurowane, ale jeszcze nie zalogowane przez Stravę
        return render_template("dashboard.html", authorized=False, athlete=None, activities=[], components=[])

    activities = storage.get_activities()
    components = storage.get_components()
    bikes = config.get("bikes", [])

    # Grupowanie komponentów po typie z sortowaniem:
    # 1. Aktywne (bez daty usunięcia) — na górze, "Od początku" na końcu aktywnych
    # 2. Wycofane (z datą usunięcia) — na dole
    components_grouped = {}
    for c in components:
        t = c.get("type", "Inne")
        components_grouped.setdefault(t, []).append(c)

    def sort_key(c):
        removed = c.get("removed", "").strip()
        added = c.get("added", "").strip()
        is_removed = 1 if removed else 0          # wycofane na dół
        is_from_start = 1 if added == "Od początku" else 0  # "Od początku" na dół wśród aktywnych
        return (is_removed, is_from_start, added)

    for t in components_grouped:
        components_grouped[t].sort(key=sort_key)

    athlete = config.get("athlete", {})
    return render_template("dashboard.html", authorized=True, athlete=athlete,
                            activities=activities, components=components,
                            components_grouped=components_grouped, bikes=bikes)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        client_id = request.form.get("client_id", "").strip()
        client_secret = request.form.get("client_secret", "").strip()
        storage.update_config(client_id=client_id, client_secret=client_secret)
        return redirect(url_for("dashboard"))

    config = storage.get_config()
    return render_template("settings.html", config=config)


@app.route("/auth/authorize")
def authorize():
    """Przekierowuje użytkownika na stronę logowania Strava."""
    config = storage.get_config()
    client_id = config.get("client_id")

    if not client_id:
        return redirect(url_for("settings"))

    redirect_uri = request.url_root.rstrip("/") + "/auth/callback"
    auth_url = strava_client.build_authorize_url(client_id, redirect_uri)
    return redirect(auth_url)


@app.route("/auth/callback")
def auth_callback():
    """Strava przekierowuje tu z powrotem po zalogowaniu, z ?code=... w URL."""
    code = request.args.get("code")
    error = request.args.get("error")

    if error:
        return f"Autoryzacja odrzucona: {error}", 400

    if not code:
        return "Brak kodu autoryzacyjnego w odpowiedzi Stravy.", 400

    config = storage.get_config()
    token_data = strava_client.exchange_code_for_token(
        config["client_id"], config["client_secret"], code
    )

    storage.update_config(
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        expires_at=token_data["expires_at"],
        athlete=token_data.get("athlete", {}),
    )

    return redirect(url_for("dashboard"))


@app.route("/components", methods=["GET", "POST"])
def components():
    if request.method == "POST":
        raw_text = request.form.get("raw_text", "")
        parsed = components_parser.parse_components_text(raw_text)
        storage.save_components(parsed)
    return redirect(url_for("dashboard") + "#components")


@app.route("/sync/bikes", methods=["POST"])
def sync_bikes():
    """Pobiera listę rowerów ze Strava API i zapisuje w config."""
    config = storage.get_config()
    access_token = _get_valid_access_token(config)

    if not access_token:
        return jsonify({"error": "Nie zalogowano"}), 401

    bikes = strava_client.get_bikes(access_token)
    storage.update_config(bikes=bikes)
    return jsonify({"message": f"Pobrano {len(bikes)} rower(ów).", "bikes": bikes})


@app.route("/sync", methods=["POST"])
def sync():
    """Pobiera aktywności ze Stravy i zapisuje lokalnie."""
    config = storage.get_config()
    access_token = _get_valid_access_token(config)

    if not access_token:
        return jsonify({"error": "Nie zalogowano"}), 401

    existing = storage.get_activities()
    existing_ids = {a["id"] for a in existing}

    page = 1
    new_count = 0
    while True:
        batch = strava_client.get_activities(access_token, page=page, per_page=100)
        if not batch:
            break
        for activity in batch:
            if activity["id"] not in existing_ids:
                existing.append(activity)
                existing_ids.add(activity["id"])
                new_count += 1
        page += 1
        if len(batch) < 100:
            break

    existing.sort(key=lambda a: a.get("start_date", ""), reverse=True)
    storage.save_activities(existing)

    return jsonify({"message": f"Zsynchronizowano. Nowych aktywności: {new_count}", "total": len(existing)})


def _get_valid_access_token(config: dict) -> str | None:
    """Zwraca ważny access_token, odświeżając go w razie potrzeby."""
    if not config.get("access_token"):
        return None

    if time.time() >= config.get("expires_at", 0):
        refreshed = strava_client.refresh_access_token(
            config["client_id"], config["client_secret"], config["refresh_token"]
        )
        storage.update_config(
            access_token=refreshed["access_token"],
            refresh_token=refreshed["refresh_token"],
            expires_at=refreshed["expires_at"],
        )
        return refreshed["access_token"]

    return config["access_token"]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
