import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID') or ''
    SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET') or ''
    SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI') or 'https://localhost:8000/callback'