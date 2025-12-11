import base64
import requests
from urllib.parse import urlparse

from typing import List, Dict, Any

SPOTIFY_CLIENT_ID = "TODO"
SPOTIFY_CLIENT_SECRET = "TODO"

def get_access_token() -> str:
    token_url = "https://accounts.spotify.com/api/token"
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64 = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    resp = requests.post(token_url, headers=headers, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]


def extract_playlist_id(playlist_url: str) -> str:
    # https://open.spotify.com/playlist/XYZ?si=... formatından ID çıkarma
    if playlist_url.startswith("spotify:playlist:"):
        return playlist_url.split(":")[2]

    try:
        parsed = urlparse(playlist_url)
        parts = parsed.path.split("/")
        if "playlist" in parts:
            idx = parts.index("playlist")
            return parts[idx + 1]
    except Exception:
        pass

    # fallback regex burada yazılabilir
    raise ValueError("Geçersiz playlist URL")


# backend tayfa burada:
# - playlist tracklerini çekecek
# - audio_features alacak
# - ortalamaları hesaplayacak
# - app.py içindeki analyze_playlist fonksiyonu bunları kullanacak
