"""
Helper functions for communicating with the Strava API.

API reference: https://developers.strava.com/docs/reference/
"""

import requests

TOKEN_URL = "https://www.strava.com/oauth/token"
AUTHORIZE_URL = "https://www.strava.com/oauth/authorize"
API_BASE = "https://www.strava.com/api/v3"


def build_authorize_url(client_id: str, redirect_uri: str) -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "approval_prompt": "force",
        "scope": "read,activity:read_all,profile:read_all",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{AUTHORIZE_URL}?{query}"


def exchange_code_for_token(client_id: str, client_secret: str, code: str) -> dict:
    """Exchanges the authorization code (from Strava redirect) for access and refresh tokens."""
    response = requests.post(TOKEN_URL, data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
    })
    response.raise_for_status()
    return response.json()


def refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> dict:
    """Refreshes the access token using the refresh token (Strava tokens expire after 6 hours)."""
    response = requests.post(TOKEN_URL, data={
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    })
    response.raise_for_status()
    return response.json()


def get_activities(access_token: str, page: int = 1, per_page: int = 100) -> list:
    """Fetches a page of the athlete's activities."""
    response = requests.get(
        f"{API_BASE}/athlete/activities",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"page": page, "per_page": per_page},
    )
    response.raise_for_status()
    return response.json()


def get_bikes(access_token: str) -> list:
    """Fetches the list of bikes for the logged-in athlete."""
    response = requests.get(
        f"{API_BASE}/athlete",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    data = response.json()
    return data.get("bikes") or []
