import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

# Load environment variables
load_dotenv()

def debug_spotify_api():
    """Debug Spotify API calls to understand the issues"""
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    
    print(f"Client ID: {client_id}")
    print(f"Client Secret length: {len(client_secret) if client_secret else 0}")
    
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
        
        print("Successfully created Spotify client")
        
        # Test 1: Basic search
        print("\n--- Test 1: Basic search ---")
        try:
            results = sp.search(q='test', type='track', limit=1)
            print(f"Search successful. Found {results['tracks']['total']} tracks")
            if results['tracks']['items']:
                test_track_id = results['tracks']['items'][0]['id']
                print(f"Test track ID: {test_track_id}")
                
                # Test 2: Single track audio features
                print("\n--- Test 2: Single track audio features ---")
                try:
                    features = sp.audio_features(test_track_id)
                    print(f"Single track audio features: {'SUCCESS' if features else 'FAILED'}")
                    if features:
                        print(f"Features received: {type(features)}")
                        if isinstance(features, list) and features:
                            print(f"First feature keys: {list(features[0].keys()) if features[0] else 'None'}")
                except Exception as e:
                    print(f"Single track audio features failed: {e}")
                
                # Test 3: Multiple tracks audio features
                print("\n--- Test 3: Multiple tracks audio features ---")
                try:
                    features = sp.audio_features([test_track_id])
                    print(f"Multiple tracks audio features: {'SUCCESS' if features else 'FAILED'}")
                    if features:
                        print(f"Features received: {type(features)}")
                        if isinstance(features, list) and features:
                            print(f"First feature keys: {list(features[0].keys()) if features[0] else 'None'}")
                except Exception as e:
                    print(f"Multiple tracks audio features failed: {e}")
                    
        except Exception as e:
            print(f"Search failed: {e}")
        
        # Test 4: Manual token request
        print("\n--- Test 4: Manual token request ---")
        try:
            auth_url = 'https://accounts.spotify.com/api/token'
            auth_response = requests.post(auth_url, {
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret,
            })
            
            if auth_response.status_code == 200:
                auth_data = auth_response.json()
                access_token = auth_data['access_token']
                print("Manual authentication successful")
                print(f"Token type: {auth_data.get('token_type')}")
                print(f"Expires in: {auth_data.get('expires_in')} seconds")
                
                # Test manual API call
                headers = {'Authorization': f'Bearer {access_token}'}
                test_track_id = '450pIumGxo4gf8bVXj4NKN'  # Known track ID
                
                # Single track endpoint
                audio_features_url = f'https://api.spotify.com/v1/audio-features/{test_track_id}'
                response = requests.get(audio_features_url, headers=headers)
                print(f"\nManual single track call status: {response.status_code}")
                if response.status_code == 200:
                    print("Manual single track call successful")
                else:
                    print(f"Manual single track call failed: {response.text}")
                
                # Multiple tracks endpoint
                audio_features_url = f'https://api.spotify.com/v1/audio-features?ids={test_track_id}'
                response = requests.get(audio_features_url, headers=headers)
                print(f"\nManual multiple tracks call status: {response.status_code}")
                if response.status_code == 200:
                    print("Manual multiple tracks call successful")
                    print(f"Response keys: {list(response.json().keys())}")
                else:
                    print(f"Manual multiple tracks call failed: {response.text}")
            else:
                print(f"Manual authentication failed: {auth_response.status_code}")
                print(auth_response.text)
        except Exception as e:
            print(f"Manual token request failed: {e}")
            
    except Exception as e:
        print(f"Error during testing: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    debug_spotify_api()