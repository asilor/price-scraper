from pymongo import MongoClient
import os


class Database:
    def __init__(self):

        mongo_ip = os.getenv("MONGO_IP")
        mongo_port = int(os.getenv("MONGO_PORT"))
        mongo_user = os.getenv("MONGO_USER")
        mongo_password = os.getenv("MONGO_PASSWORD")
        mongo_db_name = os.getenv("MONGO_DB_NAME")

        mongo_url = f"mongodb://{mongo_user}:{mongo_password}@{mongo_ip}:{mongo_port}"

        try:
            self.client = MongoClient(mongo_url)
            self.db = self.client[mongo_db_name]
            print("Database connection successful")
        except Exception as e:
            print("Connection failed:", e)
            self.client = None
            self.db = None


def iterate_collection(db: Database, collection_name: str):
    "Yields documents from a MongoDB collection."

    collection = db.db[collection_name]
    cursor = collection.find()
    
    try:
        for document in cursor:
            yield document
    finally:
        cursor.close()