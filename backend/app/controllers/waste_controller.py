from flask import request, jsonify
from ..services.eco_points_service import earn_eco_points
from ..models import WastePickup, RecyclingTracking
from .. import db

class WasteController:
    @staticmethod
    def schedule_pickup():
        data = request.get_json()
        new_pickup = WastePickup(
            user_id=data['user_id'],
            pickup_date=data['pickup_date'],
            address=data['address']
        )
        db.session.add(new_pickup)
        db.session.commit()
        earn_eco_points(data['user_id'], 10)  # Example points for scheduling
        return jsonify({"message": "Pickup scheduled successfully!"}), 201

    @staticmethod
    def track_recycling():
        data = request.get_json()
        new_tracking = RecyclingTracking(
            user_id=data['user_id'],
            material=data['material'],
            weight=data['weight'],
            date=data['date']
        )
        db.session.add(new_tracking)
        db.session.commit()
        earn_eco_points(data['user_id'], 5)  # Example points for recycling
        return jsonify({"message": "Recycling tracked successfully!"}), 201

    @staticmethod
    def get_user_pickups(user_id):
        pickups = WastePickup.query.filter_by(user_id=user_id).all()
        return jsonify([pickup.to_dict() for pickup in pickups]), 200

    @staticmethod
    def get_user_recycling(user_id):
        recycling = RecyclingTracking.query.filter_by(user_id=user_id).all()
        return jsonify([track.to_dict() for track in recycling]), 200