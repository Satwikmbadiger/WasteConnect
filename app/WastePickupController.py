from . import PickupService as pk
from flask import request, jsonify,Blueprint


waste_pickup = Blueprint('waste_pickup', __name__)

@waste_pickup.route('/getSchedule/<pickup_id>', methods=['GET'])
def get_waste_pickup(pickup_id):
    data = pk.get_schedule(pickup_id)
    
    return jsonify(data)

@waste_pickup.route('/addSchedule', methods=['POST'])
def schedule_waste_pickup():
    data = request.json
    
    if pk.add_schedule(data):
        
        return jsonify({"success": True}), 200
    
    return jsonify({"success": False}), 500
    

