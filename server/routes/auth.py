from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from motor.motor_asyncio import AsyncIOMotorClient
import zxcvbn
import bcrypt

# ------------------ Limiter ------------------
limiter = Limiter(key_func=get_remote_address)

# ------------------ App ------------------
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ MongoDB ------------------
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["users_db"]
users_collection = db["users"]

# ------------------ Auth Router ------------------
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/signup")
@limiter.limit("5/minute")
async def signup(request: Request):
    data = await request.json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    if not email or not username or not password:
        raise HTTPException(status_code=400, detail="Email, username, and password are required.")
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    if zxcvbn.zxcvbn(password)["score"] < 3:
        raise HTTPException(status_code=400, detail="Password is too weak.")
    if await users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
        raise HTTPException(status_code=400, detail="Username or email already taken.")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Invalid email format.")

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    result = await users_collection.insert_one({
        "email": email,
        "username": username,
        "password": hashed_password.decode("utf-8")
    })

    return {"id": str(result.inserted_id), "email": email, "username": username}

# ------------------ Include Router ------------------
app.include_router(auth_router, prefix="/api")