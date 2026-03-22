import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-dev-key')

    # PostgreSQL only — must be set via HF Spaces Secrets (or .env locally)
    _db_url = os.environ.get('DATABASE_URL', '')

    # Fix for older Heroku/Render/Railway style URLs
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False