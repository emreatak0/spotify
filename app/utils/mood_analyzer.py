def analyze_mood(audio_features):
    """
    Analyze the mood of tracks based on audio features
    """
    if not audio_features:
        return "Analysis Unavailable", "Unable to analyze detailed audio features. This is a known limitation with some Spotify applications where access to audio analysis endpoints is restricted. The playlist is accessible, but detailed mood analysis is not available due to API restrictions."
    
    # Filter out None values and empty dictionaries
    valid_features = [track for track in audio_features if track and isinstance(track, dict)]
    
    if not valid_features:
        return "Analysis Unavailable", "Unable to analyze detailed audio features. This is a known limitation with some Spotify applications where access to audio analysis endpoints is restricted. The playlist is accessible, but detailed mood analysis is not available due to API restrictions."
    
    # Calculate averages for key features
    avg_energy = sum([track['energy'] for track in valid_features]) / len(valid_features)
    avg_valence = sum([track['valence'] for track in valid_features]) / len(valid_features)
    avg_danceability = sum([track['danceability'] for track in valid_features]) / len(valid_features)
    avg_tempo = sum([track['tempo'] for track in valid_features]) / len(valid_features)
    avg_acousticness = sum([track['acousticness'] for track in valid_features]) / len(valid_features)
    avg_instrumentalness = sum([track['instrumentalness'] for track in valid_features]) / len(valid_features)
    
    # Determine mood based on features
    if avg_energy > 0.7 and avg_valence > 0.7:
        mood = "Energetic & Happy"
        description = f"This playlist is full of high-energy, upbeat tracks with an average tempo of {avg_tempo:.0f} BPM that will get you moving!"
    elif avg_energy > 0.7 and avg_valence <= 0.7:
        mood = "Intense"
        description = "This playlist features intense, powerful tracks with strong emotional energy. Perfect for workouts or when you need to focus."
    elif avg_energy <= 0.7 and avg_valence > 0.7:
        mood = "Cheerful"
        description = "This playlist has a positive, cheerful vibe with uplifting melodies. Great for brightening your day!"
    elif avg_danceability > 0.7:
        mood = "Danceable"
        description = f"With highly danceable tracks and an average tempo of {avg_tempo:.0f} BPM, this playlist is perfect for dancing!"
    elif avg_tempo > 120:
        mood = "Upbeat"
        description = f"Keeping the energy flowing with an average tempo of {avg_tempo:.0f} BPM, this playlist maintains an upbeat rhythm."
    elif avg_acousticness > 0.7:
        mood = "Acoustic"
        description = "This playlist features acoustic tracks with organic sounds. Perfect for relaxing or intimate moments."
    elif avg_instrumentalness > 0.5:
        mood = "Instrumental"
        description = "With predominantly instrumental tracks, this playlist is ideal for focusing or studying."
    else:
        mood = "Relaxed"
        description = "This playlist has a calm, relaxed atmosphere perfect for unwinding after a long day."
    
    return mood, description