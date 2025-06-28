import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    GITHUB_API_BASE_URL = 'https://api.github.com'
    GITHUB_API_TIMEOUT = 10
    MAX_EVENTS_DISPLAY = 50
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true' 