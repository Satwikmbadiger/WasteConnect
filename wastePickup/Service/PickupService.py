import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from wastePickup.utils import currentTime as ct
from . import userService as us
from wastePickup.config import cred

db = firestore.client()
def add_schedule(data, user):
    try:
        
        if not user or not all(key in user for key in ['id', 'name', 'location']):
            return {"message": "Missing required user information"}, 400

        # Validate pickup date
        pickup_date = data.get('pickupDate')
        if not pickup_date:
            return {"message": "Pickup date is required"}, 400

        admin_response = allocate_pickup(user.get('location'))
        if isinstance(admin_response, tuple):  # Check if it's an error response
            return admin_response  # Propagate the error

        admin_id = admin_response.get('id')
        if not admin_id:
            return {"message": "Failed to get admin ID"}, 400

        # Prepare schedule data
        schedule_data = {
            'timeStamp': ct.get_time(),
            'uid': user.get('id'),
            'name': user.get('name'),
            'location': user.get('location'),
            'status': "pending",
            'pickupDate': pickup_date,
            'adminId': admin_id
        }

        # Add schedule to Firestore
        result = db.collection('waste_pickup').add(schedule_data)
        doc_ref = result[1]

        return {"message": "Schedule added successfully", "pickup_id": doc_ref.id}, 200

    except Exception as e:
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
    
def allocate_pickup(location):
    try:
        
        if not location:
            return {"message": "Location is required"}, 400
        
        # Get all admins
        admins = us.getUserByRole('admin')
        if not admins:
            return {"message": "No admins found"}, 404
        
        # Filter admins by location
        admins_in_location = [admin for admin in admins if admin.get('location') == location]
        
        if admins_in_location:
            return admins_in_location[0]  # Return the first admin in the location
        else:
            return {"message": "No admin found for the location"}, 404
            
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500
    
# def count_pickup(user):
#     try:
#        if user.get('id')==db.collection("waste_pickup").get('uid') and db.collection("waste_pickup").get('status')=="completed":
#            user['count'] = user['count'] + 1
#            return user['count']
                   
#     except Exception as e:
#         return {"message": f"Failed to retrieve pickup count: {str(e)}"}, 500