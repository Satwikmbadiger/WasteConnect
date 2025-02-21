from datetime import datetime

class EcoPointsService:
    def __init__(self, db):
        self.db = db

    def earn_points(self, user_id, points):
        user = self.db.collection('users').document(user_id)
        user.update({
            'eco_points': firestore.Increment(points),
            'last_updated': datetime.utcnow()
        })

    def redeem_points(self, user_id, points):
        user = self.db.collection('users').document(user_id)
        user_data = user.get().to_dict()
        
        if user_data and user_data['eco_points'] >= points:
            user.update({
                'eco_points': firestore.Increment(-points),
                'last_updated': datetime.utcnow()
            })
            return True
        return False

    def get_points_balance(self, user_id):
        user = self.db.collection('users').document(user_id)
        user_data = user.get().to_dict()
        return user_data['eco_points'] if user_data else 0

    def get_user_eco_points_history(self, user_id):
        history_ref = self.db.collection('eco_points_history').where('user_id', '==', user_id)
        return history_ref.stream()