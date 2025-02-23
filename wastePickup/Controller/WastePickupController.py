from app.Service import PickupService as pk
from app.Service import userService as us

from flask import render_template, request, jsonify,Blueprint


waste_pickup = Blueprint('waste_pickup', __name__)

@waste_pickup.route('/getSchedule/<pickup_id>', methods=['GET'])
def get_waste_pickup(pickup_id):
    try:
        user = us.verify_token_and_get_user()
        if isinstance(user, tuple):
            return jsonify(user[0]), user[1]
        
        if user.get('role') == 'admin':
            data = pk.get_schedule(pickup_id)
            if isinstance(data, tuple):
                return jsonify(data[0]), data[1]
            return jsonify(data)
           # return render_template('CollectorDashboard.html', data=data)
        else:
            return jsonify({"error": "Unauthorized"}), 401
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# @waste_pickup.route('/pickupForm')
# def pickup_form():
#     return render_template('pickupinfo.html')

@waste_pickup.route('/addSchedule', methods=['POST'])
def add_schedule_route():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if 'pickupDate' not in data:
            return jsonify({"error": "Pickup date is required"}), 400
        
        user = us.verify_token_and_get_user()
        if isinstance(user, tuple):
            return jsonify(user[0]), user[1]
        
        if user.get('role')== 'admin':
            return jsonify({"error": "Unauthorized"}), 401
        
        success = pk.add_schedule(data, user)
        if isinstance(success, tuple):
            return jsonify(success[0]), success[1]
        
      
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500