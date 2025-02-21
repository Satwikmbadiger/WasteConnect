import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY')
    STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///site.db'
    ECO_POINTS_REWARD_RATE = 10  # Points earned per sustainable action