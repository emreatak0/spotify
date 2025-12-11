document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('playlist-form');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const moodResult = document.getElementById('mood-result');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const playlistUrl = document.getElementById('playlist-url').value;
        
        // Validate URL
        if (!playlistUrl || !isValidSpotifyUrl(playlistUrl)) {
            showError('Please enter a valid Spotify playlist URL');
            return;
        }
        
        // Show loading indicator
        loading.classList.remove('hidden');
        result.classList.add('hidden');
        
        // Send request to backend
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ playlist_url: playlistUrl })
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading indicator
            loading.classList.add('hidden');
            
            if (data.error) {
                showError(data.error);
            } else {
                // Display result
                displayResult(data);
            }
        })
        .catch(error => {
            // Hide loading indicator
            loading.classList.add('hidden');
            
            // Display error
            showError('Failed to analyze playlist. Please check the URL and try again.');
        });
    });
    
    function isValidSpotifyUrl(url) {
        return url.includes('spotify.com/playlist/') || url.includes('spotify:playlist:');
    }
    
    function displayResult(data) {
        // Check if this is a fallback response
        const isFallback = data.fallback === true;
        
        moodResult.innerHTML = `
            <div class="mood-card ${isFallback ? 'fallback' : ''}">
                <h3>${data.mood}</h3>
                <p class="mood-description">${data.description}</p>
                <p>Tracks in playlist: ${data.tracks_analyzed}</p>
                ${isFallback ? '<p class="note">Note: Detailed audio analysis is limited due to API restrictions. Playlist is accessible on Spotify.</p>' : ''}
                ${data.cached ? '<p class="cached">Cached result</p>' : ''}
            </div>
        `;
        result.classList.remove('hidden');
    }
    
    function showError(message) {
        moodResult.innerHTML = `
            <div class="mood-card error">
                <h3>Error</h3>
                <p class="mood-description">${message}</p>
            </div>
        `;
        result.classList.remove('hidden');
    }
});