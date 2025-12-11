from flask import Blueprint, render_template, request, jsonify
from app.services.spotify_service import SpotifyService
from app.utils.mood_analyzer import analyze_mood
from app.models.database import Database

main_bp = Blueprint('main', __name__)
spotify_service = SpotifyService()
db = Database()

@main_bp.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@main_bp.route('/analyze', methods=['POST'])
def analyze_playlist():
    """Analyze a Spotify playlist URL"""
    data = request.get_json()
    playlist_url = data.get('playlist_url')
    
    # Validate input
    if not playlist_url:
        return jsonify({'error': 'Playlist URL is required'}), 400
    
    # Check if we have a cached analysis
    cached_analysis = db.get_analysis(playlist_url)
    if cached_analysis:
        result = {
            'playlist_url': cached_analysis[1],
            'mood': cached_analysis[3],
            'description': cached_analysis[4],
            'tracks_analyzed': cached_analysis[5],
            'cached': True
        }
        return jsonify(result)
    
    # Extract playlist ID
    playlist_id = spotify_service.extract_playlist_id(playlist_url)
    
    if not playlist_id:
        return jsonify({'error': 'Invalid Spotify playlist URL'}), 400
    
    try:
        # Get playlist tracks
        tracks = spotify_service.get_playlist_tracks(playlist_id)
        
        if not tracks:
            return jsonify({'error': 'Could not fetch playlist tracks. Make sure the playlist is public and accessible.'}), 400
        
        # Extract track IDs
        track_ids = [track['track']['id'] for track in tracks if track['track'] and track['track']['id']]
        
        if not track_ids:
            return jsonify({'error': 'No valid tracks found in the playlist'}), 400
        
        # Get audio features
        audio_features = spotify_service.analyze_track_features(track_ids)
        
        # Filter out None values
        valid_features = [f for f in audio_features if f]
        
        # If we can't get audio features, provide a graceful fallback
        if not valid_features:
            # Return a simplified response without detailed mood analysis
            result = {
                'playlist_url': playlist_url,
                'mood': 'Detailed Analysis Unavailable',
                'description': 'The playlist is accessible, but detailed audio analysis is not available due to API restrictions. This is a known limitation with some Spotify applications where access to audio analysis endpoints is restricted. You can still view the playlist on Spotify.',
                'tracks_analyzed': len(track_ids),
                'cached': False,
                'fallback': True
            }
            
            # Save to database with fallback info
            db.save_analysis(playlist_url, playlist_id, 'Detailed Analysis Unavailable', 'Unable to analyze audio features due to API restrictions', len(track_ids))
            
            return jsonify(result)
        
        # Analyze mood
        mood, description = analyze_mood(valid_features)
        
        # Save to database
        db.save_analysis(playlist_url, playlist_id, mood, description, len(valid_features))
        
        # Prepare response
        result = {
            'playlist_url': playlist_url,
            'mood': mood,
            'description': description,
            'tracks_analyzed': len(valid_features),
            'cached': False
        }
        
        return jsonify(result)
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error analyzing playlist: {str(e)}")
        # Check if it's a specific Spotify error
        if 'Resource not found' in str(e) or '404' in str(e):
            return jsonify({'error': 'Could not find the playlist. Make sure the playlist URL is correct and the playlist is public.'}), 400
        elif '401' in str(e) or 'Unauthorized' in str(e):
            return jsonify({'error': 'Authentication error with Spotify API. Please contact the administrator.'}), 500
        elif '403' in str(e) or 'Forbidden' in str(e):
            return jsonify({'error': 'Access denied to the playlist. Make sure the playlist is public and accessible.'}), 400
        else:
            return jsonify({'error': 'An error occurred while analyzing the playlist. Please try again later.'}), 500