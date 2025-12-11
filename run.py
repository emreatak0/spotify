import os
import sys

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.app import app

if __name__ == "__main__":
    # Run on port 8000 to avoid conflicts
    app.run(debug=True, port=8000)