import os
import time

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from .database import users_collection

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "replace-me")
ALGORITHM = "HS256"
security = HTTPBearer()


def create_token(user_id: str):
    payload = {"user_id": user_id, "exp": int(time.time() + 3600)}  # 1h expiry
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        data = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return data["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(req: RegisterRequest):
    existing_user = await users_collection.find_one({"username": req.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt())
    await users_collection.insert_one({"username": req.username, "password": hashed_pw.decode('utf-8')})
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(req: LoginRequest):
    user = await users_collection.find_one({"username": req.username})
    if not user or not bcrypt.checkpw(req.password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token(str(user["_id"]))
    return {"token": token, "username": user["username"], "user_id": str(user["_id"])}
