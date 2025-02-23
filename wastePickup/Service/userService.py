import firebase_admin
from firebase_admin import credentials, auth,firestore
from wastePickup.config import cred
from . import PickupService as pk

db = firestore.client()

from flask import request, jsonify, current_app
import firebase_admin
from firebase_admin import auth, credentials

# def check_rewards(user):
#     try:
#      count=pk.count_pickup(user)
     
#      if count/5==0:
#          return {"message":"You have earned a reward"}

#     except Exception as e:
#         return {"error": str(e)}, 500
        
        
       

def getUserByRole(role):
    try:
        users_ref = db.collection('users')
        users = users_ref.where('role', '==', role).stream()
        
        users_list = []
        for user in users:
            user_data = user.to_dict()
            user_data['id'] = user.id
            users_list.append(user_data)
        
        return users_list
    except Exception as e:
        print(f"An error occurred while retrieving users: {str(e)}")
        return []

def verify_token_and_get_user():
    try:
         auth_header = request.headers.get('Authorization')
         if not auth_header or not auth_header.startswith('Bearer '):
             return {'error': 'No token provided'}, 401
        
         token = auth_header.split('Bearer ')[1]
        
         decoded_token = auth.verify_id_token(token)
         user_id = decoded_token['uid']
        #  user_id="5by0wd8jseT1R4u3KojS"
        
         user_snapshot = db.collection('users').document(user_id).get()
         if not user_snapshot.exists:
            return {'error': 'User not found'}, 404
        
         user_data = user_snapshot.to_dict()
         user_data['id'] = user_id
         user_data['count']=0
        
         return user_data
        
    except auth.InvalidIdTokenError:
        return {'error': 'Invalid token'}, 401
    except auth.ExpiredIdTokenError:
        return {'error': 'Expired token'}, 401
    except Exception as e:
        return {'error': str(e)}, 500
    

