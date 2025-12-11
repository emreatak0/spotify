import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load environment variables
load_dotenv()

def test_spotify_auth():
    """Test Spotify authentication and basic API access"""
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    
    print(f"Client ID: {client_id}")
    if client_secret:
        print(f"Client Secret: {client_secret[:5]}...{client_secret[-5:]}")
    else:
        print("Client Secret: None")
    
    if not client_id or not client_secret:
        print("Error: Missing Spotify credentials")
        return
    
    try:
        # Create client credentials manager
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        
        # Create Spotify client
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        # Test basic API access
        print("Testing basic API access...")
        results = sp.search(q='test', type='track', limit=1)
        print(f"Search successful. Found {results['tracks']['total']} tracks")
        
        # Test audio features access
        print("Testing audio features access...")
        # Using a known track ID for testing
        test_track_id = '450pIumGxo4gf8bVXj4NKN'  # A random track ID
        features = sp.audio_features([test_track_id])
        print(f"Audio features test: {'SUCCESS' if features else 'FAILED'}")
        if features:
            print(f"Features: {features[0] if features[0] else 'None'}")
        
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    test_spotify_auth()