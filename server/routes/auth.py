from fastapi import APIRouter, Request, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

import bcrypt

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["users_db"]
users_collection = db["users"]

@auth_router.post("/signup")
async def signup(request: Request):
    data = await request.json()
    email = data.get("email")
    username = data.get("username")
    hashed_password = bcrypt.hashpw(data.get("password").encode('utf-8'), bcrypt.gensalt())

    if not email or not username or not hashed_password:
        raise HTTPException(status_code=400, detail="Email, username, and password are required.")
    
    result = await users_collection.insert_one({
        "email": email,
        "username": username,
        "password": hashed_password.decode('utf-8')
    })
    data["id"] = str(result.inserted_id)
    print("Signup data:", data)
    return data