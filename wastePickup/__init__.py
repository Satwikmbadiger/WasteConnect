from flask import Flask
from wastePickup.config import cred

def create_app():
    app=Flask(__name__)
    
    from .Controller.WastePickupController import waste_pickup
    app.register_blueprint(waste_pickup, url_prefix='/wastepickup',template_folder='templates')
    
    
    
    
    app.config['SECRET_KEY']="befbb"
    
    return app