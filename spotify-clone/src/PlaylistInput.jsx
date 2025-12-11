import { useState } from "react";
import "./playlistInput.css"; // ← CSS'i burada çağır

export default function PlaylistInput({ onAnalyze }) {
  const [link, setLink] = useState("");

  const extractPlaylistId = (url) => {
    const regex = /playlist\/([a-zA-Z0-9]+)|spotify:playlist:([a-zA-Z0-9]+)/;
    const m = url.match(regex);
    if (!m) return null;
    return m[1] || m[2];
  };

  const handleAnalyze = () => {
    const id = extractPlaylistId(link.trim());
    if (!id) {
      alert("Geçerli bir Spotify playlist linkini yapıştırın.");
      return;
    }
    onAnalyze(id);
  };

  return (
    <div className="playlist-container">
      <input
        className="playlist-input"
        value={link}
        onChange={(e) => setLink(e.target.value)}
        placeholder="Spotify playlist linkinizi yapıştır..."
      />
      <button className="playlist-button" onClick={handleAnalyze}>
        Analiz Et
      </button>
    </div>
  );
}
