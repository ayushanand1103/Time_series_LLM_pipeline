from datetime import datetime
import bcrypt
from pymongo.errors import DuplicateKeyError
from core.database import users_collection
from bson import ObjectId


def create_user(name: str, email: str, username: str, password: str):

    if not email or not username or not password:
        return {"status": "error", "message": "Missing required fields"}

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = {
        "name": name,
        "email": email,
        "username": username,
        "password_hash": hashed,
        "created_at": datetime.utcnow(),
        "last_login": None,
        "is_active": True
    }

    try:
        users_collection.insert_one(user)
        return {"status": "success", "message": "User created"}

    except DuplicateKeyError:
        return {"status": "error", "message": "Email or username already exists"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


def login_user(email: str, password: str):
    user = users_collection.find_one({"email": email})

    if not user:
        return {"status": "error", "message": "User not found"}

    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return {"status": "error", "message": "Invalid password"}

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )

    return {
        "status": "success",
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "username": user["username"]
        }
    }


def get_user_by_id(user_id):
    try:
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
    except:
        return None

    user = users_collection.find_one({"_id": user_id})

    if not user:
        return None

    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "username": user["username"]
    }

