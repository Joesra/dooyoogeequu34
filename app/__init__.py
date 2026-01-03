"""Entry point for Flask application"""

from flask import Flask
import os
from dotenv import load_dotenv

from app.events import bp as events_bp
from app.main import bp as main_bp

def create_app():
    app = Flask(__name__)
    
    # standaard config
    app.config["FLASK_ADMIN_FLUID_LAYOUT"] = True
    app.config["SECRET_KEY"] = "DokkiePythoniAXRvULKWuFyfURRrG0YTOOTXswLJWpU"
    
    # load .env
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(dotenv_path)
    
    # HBO-ICT API configuratie
    app.config["API_URL"] = os.getenv("API_URL", "https://hbo-ict.cloud/api")
    app.config["API_KEY"] = os.getenv("API_KEY", "JE_API_KEY_HIER")
    app.config["DATABASE"] = os.getenv("DATABASE_NAME", "jouw_database_naam")
    
    # registreer blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(events_bp, url_prefix="/events")
    
    return app
