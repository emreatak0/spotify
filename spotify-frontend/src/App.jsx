import React, { useState } from "react";
import { analyzePlaylist } from "./api";

export default function App() {
  const [playlistUrl, setPlaylistUrl] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setData(null);

    if (!playlistUrl.trim()) {
      setError("Lütfen bir Spotify playlist linki gir.");
      return;
    }

    try {
      setLoading(true);
      const res = await analyzePlaylist(playlistUrl.trim());
      setData(res);
    } catch (err) {
      console.error(err);
      setError(err.message || "Bir şeyler ters gitti.");
    } finally {
      setLoading(false);
    }
  };

  const percent = (v) => Math.round(v * 100);

  return (
    <div className="app">
      <div className="card">
        {/* HEADER */}
        <header className="header">
          <div>
            <h1 className="title">Spotify Playlist Analyst</h1>
            <p className="subtitle">
              Playlist linkini yapıştır, biz senin için tempo, enerji ve mood
              analizini çıkaralım.
            </p>
          </div>
          <div className="logo-pill">
            <span className="dot" />
            <span className="logo-text">beta</span>
          </div>
        </header>

        {/* FORM */}
        <form onSubmit={handleSubmit} className="form">
          <label htmlFor="playlistUrl" className="label">
            Spotify Playlist URL
          </label>
          <div className="input-row">
            <input
              id="playlistUrl"
              type="text"
              className="input"
              placeholder="https://open.spotify.com/playlist/..."
              value={playlistUrl}
              onChange={(e) => setPlaylistUrl(e.target.value)}
            />
            <button type="submit" className="button" disabled={loading}>
              {loading ? "Analiz ediliyor..." : "Analiz Et"}
            </button>
          </div>
        </form>

        {/* ÖRNEK BUTON */}
        {!data && !error && (
          <p className="hint">
            Test etmek için{" "}
            <button
              type="button"
              className="link-button"
              onClick={() =>
                setPlaylistUrl(
                  "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
                )
              }
            >
              Today&apos;s Top Hits
            </button>{" "}
            playlist&apos;ini deneyebilirsin.
          </p>
        )}

        {/* HATA */}
        {error && <div className="alert alert-error">{error}</div>}

        {/* SONUÇLAR */}
        {data && (
          <section className="results">
            <h2 className="section-title">Analiz Sonuçları</h2>
            <p className="playlist-id">
              Playlist ID: <code>{data.playlistId}</code>
            </p>

            {/* ÖZET BADGE'LER */}
            <div className="summary">
              <span className="badge badge-energy">
                ⚡ {data.summary.energyText}
              </span>
              <span className="badge badge-mood">
                🎧 {data.summary.moodText}
              </span>
            </div>

            {/* İSTATİSTİK KARTLARI */}
            <div className="stats-grid">
              <StatCard
                label="Ortalama Tempo"
                value={`${data.stats.tempo.toFixed(1)} BPM`}
              />
              <StatCard
                label="Enerji"
                value={`${percent(data.stats.energy)}%`}
              />
              <StatCard
                label="Dans Edilebilirlik"
                value={`${percent(data.stats.danceability)}%`}
              />
              <StatCard
                label="Pozitiflik (Valence)"
                value={`${percent(data.stats.valence)}%`}
              />
            </div>

            {/* BAR GÖSTERGESİ */}
            <div className="bars">
              <StatBar
                label="Enerji"
                value={data.stats.energy}
                emoji="⚡"
              />
              <StatBar
                label="Dans Edilebilirlik"
                value={data.stats.danceability}
                emoji="🕺"
              />
              <StatBar
                label="Pozitiflik"
                value={data.stats.valence}
                emoji="😊"
              />
            </div>
          </section>
        )}
      </div>
    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="stat-card">
      <span className="stat-label">{label}</span>
      <span className="stat-value">{value}</span>
    </div>
  );
}

function StatBar({ label, value, emoji }) {
  const pct = Math.round(value * 100);
  return (
    <div className="bar-row">
      <div className="bar-header">
        <span>
          {emoji} {label}
        </span>
        <span className="bar-percent">{pct}%</span>
      </div>
      <div className="bar-track">
        <div className="bar-fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
