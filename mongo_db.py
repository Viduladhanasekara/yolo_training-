from pymongo import MongoClient
import config

_client = None


def get_collection():
    global _client
    if _client is None:
        _client = MongoClient(config.MONGO_URI)
    db = _client[config.MONGO_DB_NAME]
    return db[config.MONGO_COLLECTION]


def insert_detection(data: dict):
    """
    Insert one detection document into MongoDB Atlas.
    data keys: camera_id, timestamp, crack_type, severity,
               confidence, fps, latitude, longitude, image_path
    """
    try:
        collection = get_collection()
        collection.insert_one(dict(data))
        return True, "Saved to MongoDB."
    except Exception as e:
        return False, f"MongoDB error: {e}"
