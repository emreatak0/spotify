import sqlite3
import os

class Database:
    def __init__(self, db_path='playlist_analysis.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table for storing playlist analyses
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                playlist_url TEXT UNIQUE,
                playlist_id TEXT,
                mood TEXT,
                description TEXT,
                tracks_analyzed INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_analysis(self, playlist_url, playlist_id, mood, description, tracks_analyzed):
        """Save playlist analysis to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO analyses 
                (playlist_url, playlist_id, mood, description, tracks_analyzed)
                VALUES (?, ?, ?, ?, ?)
            ''', (playlist_url, playlist_id, mood, description, tracks_analyzed))
            
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return None
        finally:
            conn.close()
    
    def get_analysis(self, playlist_url):
        """Retrieve playlist analysis from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM analyses WHERE playlist_url = ?
            ''', (playlist_url,))
            
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving analysis: {e}")
            return None
        finally:
            conn.close()