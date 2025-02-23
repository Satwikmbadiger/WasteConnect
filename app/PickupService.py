import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from .utils import currentTime as ct
from . import userService as us
from app.config import cred

db = firestore.client()
def add_schedule(data,user):
    data['timeStamp']=ct.get_time()
    data['uid']=user.get('id')
    data['name']=user.get('name')
    data['location']=user.get('location')
    data['status']="pending"
        
    
    try:
        db.collection('waste_pickup').add(data)
        return True
    except Exception as e:
        print(e)
        return 
    
def add_schedule(data, user):
    try:
        schedule_data = {
            'timeStamp': ct.get_time(),
            'uid': user.get('id'),
            'name': user.get('name'),
            'location': user.get('location'),
            'status': "pending",
            'pickupDate': data.get('pickupDate')
        }
        
        db.collection('waste_pickup').add(schedule_data)
        return True
    except Exception as e:
        print(f"Error adding schedule: {e}")
        return False
    
def allocate_pickup():
    try:
        docs = db.collection("waste_pickup").where("status", "==", "pending").stream()
        docs=docs.to_dict()
        
        for doc in docs:
            if doc.get('location')==db.collection('waste_pickup').document('location').get():
                return us.getUserByRole('admin')
                
        return {"error": "No such document!"}, 404
            
        
        
    except Exception as e:
        return {"error": str(e)}, 500


