import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime


cred = credentials.Certificate('app/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
def add_schedule(data):
    data['timeStamp']=get_time()
    
    
    try:
        db.collection('waste_pickup').add(data)
        return True
    except Exception as e:
        print(e)
        return False
    
def get_schedule(pickup_id):
    try:
        doc = db.collection("waste_pickup").document(pickup_id).get()
        if doc.exists:
            return doc.to_dict()
        else:
            return {"error": "No such document!"}, 404
    except Exception as e:
        return {"error": str(e)}, 500


def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")