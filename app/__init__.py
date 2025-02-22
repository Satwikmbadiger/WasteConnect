from flask import Flask

def create_app():
    app=Flask(__name__)
    
    from .WastePickupController import waste_pickup
    app.register_blueprint(waste_pickup, url_prefix='/wastepickup')
    
    
    app.config['SECRET_KEY']="befbb"
    
    return app