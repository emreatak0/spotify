import os
import sys
from flask import Flask
from app.config.config import Config

def create_app():
    # Get the absolute path to the app directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Print debug information
    print(f"App directory: {app_dir}")
    print(f"Template folder: {os.path.join(app_dir, 'templates')}")
    print(f"Static folder: {os.path.join(app_dir, 'static')}")
    
    # Configure template and static folders with absolute paths
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    
    # Configuration
    app.config.from_object(Config)
    
    # Register blueprints
    from app.controllers.main_controller import main_bp
    app.register_blueprint(main_bp)
    
    return app

app = create_app()