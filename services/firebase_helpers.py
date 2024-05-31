from firebase_config import db
def get_user_document_by_key(user_key):
    try:
        user_ref = db.collection("users").where('UserKey', '==', user_key).limit(1)
        users = user_ref.get()
        for doc in users:
            return doc.id, doc.to_dict()
    except Exception as e:
        print(f"Error finding user document by key: {e}")
    return None, None
def get_user_physical_details_by_user_key(user_key):
    try:
        user_ref = db.collection("users").where('UserKey', '==', user_key).limit(1)
        users = user_ref.get()
        for doc in users:
            user_data = doc.to_dict()
            physical_details = user_data.get('physical_details', {})
            return physical_details
    except Exception as e:
        print(f"Error finding user physical details by key: {e}")
    return None