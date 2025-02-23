from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='hjkjhjk'
    

    return app
