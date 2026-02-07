# routes/auth.py
from fastapi import APIRouter, Request, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from slowapi import Limiter
from slowapi.util import get_remote_address
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
import re
import zxcvbn
import bcrypt
import jwt
import datetime
import os
import uuid

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

limiter = Limiter(key_func=get_remote_address)
auth_router = APIRouter(prefix="/auth", tags=["auth"])

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["users_db"]
users_collection = db["users"]

USERNAME_REGEX = r"^[a-zA-Z0-9_]{3,20}$"


def generate_jwt(user_id: str, username: str):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "username": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def send_verification_email(user_email: str, verification_token: str):
    msg = EmailMessage()
    verify_link = f"http://localhost:5173/verify?token={verification_token}"
    msg.set_content(f"Click the link to verify your account:\n{verify_link}")
    msg["Subject"] = "Verify your account"
    msg["From"] = EMAIL_USER
    msg["To"] = user_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)


@auth_router.post("/signup")
@limiter.limit("5/minute")
async def signup(request: Request):
    data = await request.json()
    
    email = (data.get("email") or "").strip()
    username = (data.get("username") or "").strip()
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    # ------------------ Validations ------------------
    if not email or not username or not password:
        raise HTTPException(status_code=400, detail="Email, username, and password are required.")

    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    if not re.match(USERNAME_REGEX, username):
        raise HTTPException(
            status_code=400,
            detail="Username must be 3–20 characters, letters, numbers, underscores only."
        )

    if zxcvbn.zxcvbn(password)["score"] < 3:
        raise HTTPException(status_code=400, detail="Password is too weak.")

    try:
        validate_email(email)
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=str(e))

    existing_user = await users_collection.find_one({"$or": [{"username": username}, {"email": email}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already taken.")

    # ------------------ Hash Password ------------------
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # ------------------ Generate Verification Token ------------------
    verification_token = str(uuid.uuid4())

    # ------------------ Insert User ------------------
    result = await users_collection.insert_one({
        "email": email,
        "username": username,
        "password": hashed_password,
        "verified": False,
        "verification_token": verification_token
    })

    # ------------------ Send Verification Email ------------------
    send_verification_email(email, verification_token)

    return {
        "id": str(result.inserted_id),
        "email": email,
        "username": username,
        "message": "Signup successful! Please verify your email to activate your account."
    }


@auth_router.get("/verify")
async def verify_email(token: str):
    user = await users_collection.find_one({"verification_token": token})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token.")

    if user.get("verified"):
        return {"message": "Account already verified."}

    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"verified": True}, "$unset": {"verification_token": ""}}
    )

    # Generate JWT token after verification
    jwt_token = generate_jwt(str(user["_id"]), user["username"])
    return {"message": "Email verified successfully!", "token": jwt_token}