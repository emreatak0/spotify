import React, { useState } from "react";
import { Play, Pause, SkipBack, SkipForward } from "lucide-react";
import "./player.css";

export default function Player() {
  const [playing, setPlaying] = useState(false);

  const songs = [
    { id: 1, title: "Song A", artist: "Artist A", time: "3:21" },
    { id: 2, title: "Song B", artist: "Artist B", time: "2:50" },
    { id: 3, title: "Song C", artist: "Artist C", time: "4:10" }
  ];

  return (
    <div className="app-container">

      {/* MAIN */}
      <main className="main">
        <section className="content">

          {/* Playlist Cards */}
          <div className="playlist-section">
            <div className="playlist-grid">
              {songs.map(song => (
                <div key={song.id} className="playlist-card">
                  <button className="play-btn">
                    <Play className="icon-sm" />
                  </button>
                </div>
              ))}

              {/* Empty Card */}
              <div className="empty-card">
                <div className="empty-inner">
                  <div className="empty-icon">+</div>
                  <p>Create Playlist</p>
                </div>
              </div>
            </div>
          </div>

          {/* RIGHT COLUMN */}
          <aside className="right-column">
            <h4>Queue</h4>

            <ul className="queue-list">
              {songs.map(s => (
                <li key={s.id} className="queue-item">
                  <div>
                    <div className="queue-title">{s.title}</div>
                    <div className="queue-artist">{s.artist}</div>
                  </div>
                  <div className="queue-time">{s.time}</div>
                </li>
              ))}
            </ul>

            <div className="suggest-box">
              <h5>Suggested</h5>
              <div className="suggest-grid">
                <div className="suggest-item">Lo-fi</div>
                <div className="suggest-item">Indie</div>
                <div className="suggest-item">Electronic</div>
                <div className="suggest-item">Hip-Hop</div>
              </div>
            </div>
          </aside>
        </section>
      </main>

      {/* PLAYER BAR */}
      <footer className="player-bar">
        <div className="player-left">
          <img
            src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=200&auto=format&fit=crop"
            alt="cover"
            className="cover-img"
          />

          <div>
            <div className="song-title">Sunrise Drive</div>
            <div className="song-artist">K.Y.</div>
          </div>
        </div>

        <div className="player-center">
          <div className="controls">
            <button><SkipBack className="icon-md" /></button>

            <button
              onClick={() => setPlaying(!playing)}
              className="play-toggle"
            >
              {playing
                ? <Pause className="icon-md" />
                : <Play className="icon-md" />
              }
            </button>

            <button><SkipForward className="icon-md" /></button>
          </div>

          <input type="range" className="timeline" />
        </div>

        <div className="player-right">
          <div className="device">Device: Web</div>
          <div>Vol</div>
          <input type="range" className="volume" />
        </div>
      </footer>
    </div>
  );
}
