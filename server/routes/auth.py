from fastapi import APIRouter, Request, HTTPException, Depends, Limiter, RateLimiter
from motor.motor_asyncio import AsyncIOMotorClient
from zxcvbn import zxcvbn

import bcrypt

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["users_db"]
users_collection = db["users"]

@auth_router.post("/signup", dependencies=[Depends(RateLimiter(times=5, seconds=60))])  # Limit to 5 requests per minute
async def signup(request: Request):
    data = await request.json()

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    zxcvbn_result = zxcvbn(password)

    if not email or not username or not password:
        raise HTTPException(status_code=400, detail="Email, username, and password are required.")
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    if zxcvbn_result["score"] < 3:
        raise HTTPException(status_code=400, detail="Password is too weak.")
    # Check if user exists
    if await users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
        raise HTTPException(status_code=400, detail="Username or email already taken.")

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Insert into DB
    result = await users_collection.insert_one({
        "email": email,
        "username": username,
        "password": hashed_password.decode("utf-8")
    })

    # Return user info (without password)
    return {
        "id": str(result.inserted_id),
        "email": email,
        "username": username
    }