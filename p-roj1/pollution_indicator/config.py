import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-123'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///pollution.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Keys (Placeholders - User should provide these in .env)
    # OpenWeatherMap is highly recommended for real-time air pollution data
    OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY') or 'YOUR_OPEN_WEATHER_API_KEY'
    
    # NASA Earthdata / ESA Sentinel / Copernicus (Placeholder for headers or basic auth)
    NASA_API_KEY = os.environ.get('NASA_API_KEY') or 'YOUR_NASA_API_KEY'
