# Spotify Playlist Mood Analyzer

A web application that analyzes the mood and energy of Spotify playlists using the Spotify Web API.

## Features

- Analyze any public Spotify playlist
- Get detailed mood and energy analysis
- No user registration required
- Results cached for faster subsequent analysis

## Prerequisites

- Python 3.6 or higher
- Spotify Developer Account

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd spotify-playlist-analyzer
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Register your application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard):
   - Click "Create an App"
   - Give your app a name and description
   - Note down your Client ID and Client Secret

5. Configure environment variables:
   - Copy `.env.example` to `.env`:
     ```
     cp .env.example .env
     ```
   - Edit `.env` and fill in your Spotify credentials:
     ```
     SPOTIPY_CLIENT_ID=your_client_id_here
     SPOTIPY_CLIENT_SECRET=your_client_secret_here
     SPOTIPY_REDIRECT_URI=https://localhost:8000/callback
     SECRET_KEY=your_secret_key_here
     ```

6. Run the application:
   ```
   python run.py
   ```

7. Open your browser and go to `http://localhost:8000`

## Spotify API Setup

Spotify requires HTTPS redirect URIs for security. For local development, you have two options:

### Option 1: Use localhost with HTTPS (Recommended)
Use `https://localhost:8000/callback` as your redirect URI in the Spotify Developer Dashboard.

### Option 2: Use ngrok for HTTPS tunneling
If you encounter issues with localhost HTTPS:
1. Install ngrok: `npm install -g ngrok` or download from https://ngrok.com/
2. Run your Flask app: `python run.py`
3. In another terminal, run: `ngrok http 8000`
4. Use the HTTPS URL provided by ngrok as your redirect URI

## Usage

1. Find a public Spotify playlist
2. Copy the playlist URL
3. Paste it into the input field on the homepage
4. Click "Analyze Playlist"
5. View the mood analysis results

## How It Works

The application uses the Spotify Web API to fetch playlist data and audio features for each track. It then analyzes these features to determine the overall mood and energy of the playlist.

Audio features analyzed include:
- Energy
- Valence (musical positiveness)
- Danceability
- Tempo
- Acousticness
- Instrumentalness

## Troubleshooting

If you encounter the "redirect URI is not secure" error:
1. Make sure you're using `https://` in your redirect URI
2. Ensure the URI in your `.env` file matches exactly with the one in Spotify Dashboard
3. Consider using ngrok for HTTPS tunneling if localhost doesn't work

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.