from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import AuthController
from app.controllers.waste_controller import WasteController
from app.controllers.marketplace_controller import MarketplaceController

api = Blueprint('api', __name__)

auth_controller = AuthController()
waste_controller = WasteController()
marketplace_controller = MarketplaceController()

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    return auth_controller.login(data)

@api.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    return auth_controller.register(data)

@api.route('/waste/schedule', methods=['POST'])
def schedule_pickup():
    data = request.json
    return waste_controller.schedule_pickup(data)

@api.route('/waste/tracking', methods=['GET'])
def track_recycling():
    user_id = request.args.get('user_id')
    return waste_controller.track_recycling(user_id)

@api.route('/marketplace/products', methods=['GET'])
def get_products():
    return marketplace_controller.get_products()

@api.route('/marketplace/purchase', methods=['POST'])
def purchase_product():
    data = request.json
    return marketplace_controller.purchase_product(data)