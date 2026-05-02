from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import uuid
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

active_tokens = set()

class LoginRequest(BaseModel):
    username: str
    password: str

class MTXAuthRequest(BaseModel):
    user: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    ip: Optional[str] = None
    action: Optional[str] = None
    path: Optional[str] = None
    protocol: Optional[str] = None
    id: Optional[str] = None       
    query: Optional[str] = None

@app.post("/login")
async def login(req: LoginRequest):
    # Verify personnel credentials
    if req.username == "admin" and req.password == "admin":
        new_token = str(uuid.uuid4())
        active_tokens.add(new_token)
        print(new_token)
        return {"token": new_token}
    raise HTTPException(status_code=401, detail="Subject identification failed.")

@app.post("/auth_check")
async def auth_check(auth: MTXAuthRequest):
    print("--- NEW AUTH ATTEMPT ---")
    print(f"Full payload from MTX: {auth.dict()}") # Посмотрим всё
    print(f"Looking for token: '{auth.query[5:]}'")
    print(f"Tokens in storage: {active_tokens}")

    # Очищаем токен от возможных пробелов, которые могут затесаться
    incoming_token = auth.query.strip()[5:] if auth.query[5:] else ""

    if incoming_token in active_tokens:
        print("RESULT: SUCCESS")
        return {"status": "ok"}
    
    print("RESULT: FAILED - Token not found in active_tokens")
    raise HTTPException(status_code=403, detail="Unauthorized")