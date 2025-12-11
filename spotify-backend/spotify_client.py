import os
import requests
from typing import List, Dict, Optional
from math import isnan

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"

def get_access_token(client_id: str, client_secret: str) -> Optional[str]:
	# İstemci kimlik bilgileri ile client_credentials token al
	if not client_id or not client_secret:
		return None
	resp = requests.post(
		SPOTIFY_TOKEN_URL,
		data={"grant_type": "client_credentials"},
		auth=(client_id, client_secret),
		timeout=10,
	)
	if resp.status_code != 200:
		return None
	return resp.json().get("access_token")

def get_playlist_tracks(playlist_id: str, token: str) -> List[Dict]:
	# Tüm track item'larını sayfalandırarak çek
	items = []
	url = f"{SPOTIFY_API_BASE}/playlists/{playlist_id}/tracks"
	headers = {"Authorization": f"Bearer {token}"}
	params = {"fields": "items(track(id)),next", "limit": 100}
	while url:
		r = requests.get(url, headers=headers, params=params, timeout=10)
		if r.status_code != 200:
			raise RuntimeError(f"Spotify tracks fetch failed: {r.status_code}")
		j = r.json()
		for it in j.get("items", []):
			track = it.get("track")
			if track and track.get("id"):
				items.append(track)
		url = j.get("next")
		# params sadece ilk çağrıda anlamlı, sonrası next tam url
		params = None
	return items

def get_audio_features_for_tracks(track_ids: List[str], token: str) -> List[Dict]:
	# Max 100 id ile çağrı yapan chunked fonksiyon
	if not track_ids:
		return []
	headers = {"Authorization": f"Bearer {token}"}
	features = []
	for i in range(0, len(track_ids), 100):
		chunk = track_ids[i : i + 100]
		ids = ",".join(chunk)
		url = f"{SPOTIFY_API_BASE}/audio-features"
		r = requests.get(url, headers=headers, params={"ids": ids}, timeout=10)
		if r.status_code != 200:
			raise RuntimeError(f"Spotify audio-features failed: {r.status_code}")
		j = r.json()
		features.extend([f for f in j.get("audio_features", []) if f])
	return features

def average(values: List[float]) -> Optional[float]:
	vs = [v for v in values if v is not None]
	if not vs:
		return None
	return sum(vs) / len(vs)

def analyze_playlist(playlist_id: str, client_id: str, client_secret: str) -> Dict:
	token = get_access_token(client_id, client_secret)
	if not token:
		raise RuntimeError("Failed to obtain Spotify access token")

	tracks = get_playlist_tracks(playlist_id, token)
	track_ids = [t["id"] for t in tracks if t.get("id")]
	if not track_ids:
		return {"playlistId": playlist_id, "stats": {}, "summary": {"energyText": "Veri yok", "moodText": ""}}

	features = get_audio_features_for_tracks(track_ids, token)

	tempos = [f.get("tempo") for f in features if f]
	energies = [f.get("energy") for f in features if f]
	dance = [f.get("danceability") for f in features if f]
	valence = [f.get("valence") for f in features if f]

	avg_tempo = average(tempos)
	avg_energy = average(energies)
	avg_dance = average(dance)
	avg_valence = average(valence)

	# Basit özet oluşturma
	energy_pct = int((avg_energy or 0) * 100)
	mood = "pozitif" if (avg_valence or 0) >= 0.5 else "daha melankolik"
	energy_text = f"Ortalama enerji %{energy_pct}."
	mood_text = f"Genel hava: {mood}."

	return {
		"playlistId": playlist_id,
		"stats": {
			"tempo": round(avg_tempo, 2) if avg_tempo is not None else None,
			"energy": round(avg_energy, 2) if avg_energy is not None else None,
			"danceability": round(avg_dance, 2) if avg_dance is not None else None,
			"valence": round(avg_valence, 2) if avg_valence is not None else None,
		},
		"summary": {
			"energyText": energy_text,
			"moodText": mood_text,
		},
	}
