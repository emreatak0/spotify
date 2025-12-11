from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import os

app = Flask(__name__)
# CORS'u sadece frontend originlerine izin verecek şekilde sınırla
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

# Yeni yardımcı fonksiyon: playlistUrl'den playlistId çıkarır
def extract_playlist_id(playlist_url: str) -> str | None:
	if not playlist_url:
		return None
	# Örnek desteklenen formatlar:
	# https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=...
	# spotify:playlist:37i9dQZF1DXcBWIGoYBM5M
	m = re.search(r"playlist[/:]([A-Za-z0-9]+)", playlist_url)
	if m:
		return m.group(1)
	return None

# Yeni: Spotify entegrasyonu yalnızca gerekli env değişkenleri varsa kullanılsın
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
use_spotify = bool(SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET)

if use_spotify:
	# Yerel modül
	from spotify_client import analyze_playlist as analyze_with_spotify
else:
	analyze_with_spotify = None

@app.route("/api/health", methods=["GET"])
def health():
	return jsonify({"status": "ok"}), 200

@app.route("/api/analyze", methods=["POST"])
def analyze_playlist():
	data = request.get_json(silent=True) or {}
	playlist_url = data.get("playlistUrl")

	if not playlist_url:
		return jsonify({"error": "playlistUrl is required"}), 400

	# playlistId çıkarılıyor
	playlist_id = extract_playlist_id(playlist_url)
	if not playlist_id:
		return jsonify({"error": "Geçersiz playlistUrl formatı"}), 400

	# Eğer env ile sağlanmışsa gerçek Spotify API'yi kullan
	if use_spotify and analyze_with_spotify:
		try:
			result = analyze_with_spotify(playlist_id, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
			return jsonify(result), 200
		except Exception as e:
			# Hata oluşursa debugging için mesaj ver, frontend mock ile devam edebilir
			return jsonify({"error": "Spotify API hatası", "detail": str(e)}), 502

	# TODO: burada playlistId ile gerçek Spotify API çağrısı yapılacak.
	# Şimdilik frontend testleri için mock data dönüyoruz.
	mock_response = {
		"playlistId": playlist_id,
		"stats": {
			"tempo": 122.5,
			"energy": 0.81,
			"danceability": 0.75,
			"valence": 0.62,
		},
		"summary": {
			"energyText": f"Bu playlist çok enerjik (%{int(0.81*100)}) ⚡",
			"moodText": "Genel olarak hareketli ve pozitif bir vibe var 🎧",
		},
	}

	return jsonify(mock_response), 200

if __name__ == "__main__":
	app.run(debug=True, port=5000)
