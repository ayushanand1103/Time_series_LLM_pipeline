from pymongo import MongoClient
from pymongo.errors import PyMongoError


MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "Time_Forge"
try :
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    client.admin.command("ping")
    print("Mongo connected")

except PyMongoError as e:
    print(f" MongoDB connection failed: {e}")
    raise 

users_collection = db["users"]

