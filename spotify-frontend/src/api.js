// ŞİMDİLİK MOCK API
// Gerçek backend geldiğinde bu dosyayı değiştireceğiz.

export async function analyzePlaylist(playlistUrl) {
  // Playlist url gelmiş mi diye basit bir kontrol
  if (!playlistUrl) {
    throw new Error("playlistUrl required");
  }

  // Sırf “yükleniyor” animasyonu görünsün diye küçük bekleme
  await new Promise((res) => setTimeout(res, 800));

  // Sanki backend'den gelmiş gibi mock data dönüyoruz
  return {
    playlistId: "mock_" + Math.random().toString(36).slice(2, 8),
    stats: {
      tempo: 123.4,
      energy: 0.82,
      danceability: 0.76,
      valence: 0.61,
    },
    summary: {
      energyText: "Bu playlist çok enerjik (%82) ⚡",
      moodText: "Genel olarak hareketli ve pozitif bir vibe var 🎧",
    },
  };
}
