import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

class SpotifyService:
    def __init__(self):
        client_id = os.environ.get('SPOTIPY_CLIENT_ID')
        client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
        
        # Use Client Credentials Flow for accessing public data
        if client_id and client_secret:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=client_id, 
                client_secret=client_secret
            )
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        else:
            # Fallback to basic spotipy initialization
            self.sp = spotipy.Spotify()
    
    def extract_playlist_id(self, playlist_url):
        """Extract playlist ID from Spotify URL"""
        # Handle different URL formats
        if 'spotify.com/playlist/' in playlist_url:
            playlist_id = playlist_url.split('spotify.com/playlist/')[-1].split('?')[0]
            return playlist_id
        elif 'spotify:playlist:' in playlist_url:
            return playlist_url.split('spotify:playlist:')[-1]
        return None
    
    def get_playlist_tracks(self, playlist_id):
        """Get tracks from a playlist"""
        try:
            results = self.sp.playlist_tracks(playlist_id)
            return results['items']
        except Exception as e:
            print(f"Error fetching playlist tracks: {e}")
            # Re-raise the exception so the controller can handle it appropriately
            raise e
    
    def analyze_track_features(self, track_ids):
        """Get audio features for tracks"""
        try:
            # Filter out None values
            valid_track_ids = [tid for tid in track_ids if tid]
            
            if not valid_track_ids:
                return []
            
            # Split track_ids into chunks of 100 (Spotify API limit)
            features = []
            for i in range(0, len(valid_track_ids), 100):
                chunk = valid_track_ids[i:i+100]
                # Use audio_features without parameter name for positional argument
                chunk_features = self.sp.audio_features(chunk)
                if chunk_features:
                    # Filter out None values from the response
                    filtered_features = [f for f in chunk_features if f is not None]
                    features.extend(filtered_features)
            return features
        except Exception as e:
            print(f"Error fetching audio features: {e}")
            # Return empty list to allow fallback processing
            return []