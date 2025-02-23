import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from .utils import currentTime as ct
from . import userService as us
from app.config import cred

db = firestore.client()

def add_schedule(data, user):
    try:
        # Get admin allocation using the user's location
        admin_response = allocate_pickup(user)
        if isinstance(admin_response, tuple):  # Error response from allocation
            return {"message": admin_response[0].get('message')}, admin_response[1]
            
        admin_id = admin_response.get('id')
        if not admin_id:
            return {"message": "Failed to get admin ID"}, 400

        # Validate required user data
        if not all(key in user for key in ['id', 'name', 'location']):
            return {"message": "Missing required user information"}, 400
            
        # Validate pickup date
        pickup_date = data.get('pickupDate')
        if not pickup_date:
            return {"message": "Pickup date is required"}, 400

        schedule_data = {
            'timeStamp': ct.get_time(),
            'uid': user.get('id'),
            'name': user.get('name'),
            'location': user.get('location'),
            'status': "pending",
            'pickupDate': pickup_date,
            'adminId': admin_id
        }
        
        # Use Firestore's add() which returns a tuple: (DocumentReference, write_time)
        result = db.collection('waste_pickup').add(schedule_data)
        doc_ref = result[0]  # DocumentReference object
        return {"message": "Schedule added successfully", "id": doc_ref.id}, 200

    except Exception as e:
        print(f"Error adding schedule: {e}")
        return {"message": f"Failed to add schedule: {str(e)}"}, 500 
    
    
def get_schedule(pickup_id):
    try:
        doc = db.collection("waste_pickup").document(pickup_id).get()
        if doc.exists:
            return doc.to_dict()
        else:
            return {"error": "No such document!"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    
def allocate_pickup(user):
    try:
        location = user.get('location')
        if not location:
            return {"message": "Location is required"}, 400
        
        admin_docs = us.getUserByRole('admin').where('location', '==', location).stream()
        admins = []
        for admin in admin_docs:
            admin_data = admin.to_dict()
            # Include the document ID from the snapshot
            admin_data['id'] = admin.id
            admins.append(admin_data)
        
        if admins:
            return admins[0]
        else:
            return {"message": "No admin found for the location"}, 404
            
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500