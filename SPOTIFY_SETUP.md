# Spotify Developer Dashboard Setup Guide

To use this application, you need to register it on the Spotify Developer Dashboard to get API credentials.

## Step-by-step Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

2. Log in with your Spotify account or create a new one

3. Click "Create an App" button

4. Fill in the application details:
   - App name: Spotify Playlist Mood Analyzer
   - App description: Analyzes the mood and energy of Spotify playlists
   - Click "Create"

5. Once created, click on your new app to view its details

6. Click "Edit Settings"

7. In the "Redirect URIs" section, add this URI:
   ```
   https://localhost:8000/callback
   ```
   
   Alternatively, if you're using ngrok for development:
   ```
   https://your-ngrok-url.ngrok.io/callback
   ```

8. Click "Add" and then "Save" at the bottom

9. Note down your:
   - Client ID
   - Client Secret

10. Update your `.env` file with these credentials:
    ```
    SPOTIPY_CLIENT_ID=your_actual_client_id
    SPOTIPY_CLIENT_SECRET=your_actual_client_secret
    ```

## Important Notes

- Spotify requires HTTPS redirect URIs for security
- For local development, `https://localhost:8000/callback` is acceptable
- For production deployment, you'll need a proper SSL certificate
- Keep your Client Secret secure and never share it publicly
- The app uses Client Credentials Flow which doesn't require user authentication

## Using ngrok for HTTPS Tunneling (Alternative Method)

If you encounter issues with localhost HTTPS, you can use ngrok:

1. Install ngrok: Download from https://ngrok.com/ or use npm:
   ```
   npm install -g ngrok
   ```

2. Run your Flask app on port 8000:
   ```
   python run.py
   ```

3. In another terminal, run:
   ```
   ngrok http 8000
   ```

4. Copy the HTTPS URL provided by ngrok (looks like `https://abcd1234.ngrok.io`)

5. Update your Spotify app settings with this URL + `/callback`:
   ```
   https://abcd1234.ngrok.io/callback
   ```

6. Update your `.env` file with the same URL:
   ```
   SPOTIPY_REDIRECT_URI=https://abcd1234.ngrok.io/callback
   ```