# spotify
# Spotify Playlist Analyst 🎧

Bu proje, kullanıcıdan alınan bir **Spotify playlist linkini** analiz ederek:

- Playlist’teki şarkıları çeker,
- Her şarkı için **audio features** verilerini toplar (tempo, energy, danceability, valence vs.),
- Bu verilerden ortalamalar ve basit istatistikler üretir,
- Frontend tarafında bu istatistikleri **badge’ler** ve **grafikler** ile gösterir.

## 1. Genel Akış

1. Kullanıcı frontend’de bir **Spotify playlist URL**’si girer.
2. Frontend bu URL’yi backend’e gönderir.
3. Backend:
   - URL’den **playlist ID**’yi çıkarır,
   - Spotify Web API ile playlist’teki şarkıları alır,
   - Tüm şarkılar için **audio features** verilerini çeker,
   - Ortalama:
     - tempo (BPM),
     - energy,
     - danceability,
     - valence
     gibi değerleri hesaplar.
4. Backend, bu istatistikleri ve kısa yorumları JSON olarak frontend’e döner.
5. Frontend:
   - Yüzdelik göstergeler (badge / progress bar),
   - Grafik (örneğin radar veya bar chart)
   ile kullanıcıya playlist’in “karakterini” gösterir.

---

## 2. Teknoloji Stack’i

> Not: Buradaki stack öneri; proje başında netleştirip gerekiyorsa güncelleyin.

### Backend & API (Team Backend)

- Node.js
- Dotenv (.env yönetimi için)

### Frontend & API Bağlantıları (Team Frontend)

- React
- Fetch API veya Axios
- Chart kütüphanesi:  
  - Örn: `react-chartjs-2` + `chart.js` veya `recharts`
- UI (isteğe göre):
  - TailwindCSS / Chakra UI / MUI vs.

