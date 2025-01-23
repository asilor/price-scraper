from pymongo import MongoClient
from pymongo.database import Database
import os


def get_database() -> Database:
    """Get MongoDB database instance."""

    mongo_ip = os.getenv("MONGO_IP")
    mongo_port = int(os.getenv("MONGO_PORT"))
    mongo_user = os.getenv("MONGO_USER")
    mongo_password = os.getenv("MONGO_PASSWORD")
    mongo_db_name = os.getenv("MONGO_DB_NAME")

    connection_string = f"mongodb://{mongo_user}:{mongo_password}@{mongo_ip}:{mongo_port}"
    
    try:
        client = MongoClient(connection_string)
        db = client[mongo_db_name]
        print("Database connection successful")
        return db
    except Exception as e:
        print("Connection failed:", e)
        raise


def iterate_collection(db: Database, collection_name: str):
    "Yields documents from a MongoDB collection."

    collection = db[collection_name]
    cursor = collection.find()
    
    try:
        for document in cursor:
            yield document
    finally:
        cursor.close()


def create_prices_timeseries_collection(db: Database) -> None:
    """Create a timeseries collection for prices."""
    
    db.create_collection(
        "prices",
        timeseries={
            "timeField": "timestamp",
            "metaField": "metadata",
            "granularity": "minutes"
        }
    )