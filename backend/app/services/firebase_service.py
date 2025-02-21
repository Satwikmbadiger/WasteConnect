from firebase_admin import credentials, initialize_app, auth, firestore

# Initialize Firebase app
cred = credentials.Certificate('path/to/your/firebase/credentials.json')
initialize_app(cred)

db = firestore.client()

def create_user(email, password):
    user = auth.create_user(email=email, password=password)
    return user.uid

def get_user(uid):
    user = auth.get_user(uid)
    return user

def update_user(uid, **kwargs):
    user = auth.update_user(uid, **kwargs)
    return user

def delete_user(uid):
    auth.delete_user(uid)

def add_data(collection, document, data):
    db.collection(collection).document(document).set(data)

def get_data(collection, document):
    doc = db.collection(collection).document(document).get()
    return doc.to_dict() if doc.exists else None

def update_data(collection, document, data):
    db.collection(collection).document(document).update(data)

def delete_data(collection, document):
    db.collection(collection).document(document).delete()