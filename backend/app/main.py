from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# THIS IS CRITICAL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, allow everything. For prod, put your URL.
    allow_credentials=True,
    allow_methods=["*"], # This allows POST, OPTIONS, GET, etc.
    allow_headers=["*"],
)
# Temporary store for subject tokens
active_tokens = set()

class LoginRequest(BaseModel):
    username: str
    password: str

# This model matches the JSON schema in your .yml file comments
class MTXAuthRequest(BaseModel):
    user: str
    password: str
    token: Optional[str]
    ip: str
    action: str
    path: str
    protocol: str
    id: str
    query: str

@app.post("/login")
async def login(req: LoginRequest):
    # Verify personnel credentials
    if req.username == "admin" and req.password == "admin":
        new_token = str(uuid.uuid4())
        active_tokens.add(new_token)
        return {"token": new_token}
    raise HTTPException(status_code=401, detail="Subject identification failed.")

@app.post("/auth_check")
async def auth_check(auth: MTXAuthRequest):
    # MediaMTX sends the token/username in the 'user' field 
    # when you connect via: http://host:8889/stream?user=TOKEN
    if auth.user in active_tokens:
        print(f"Personnel {auth.user} authorized for {auth.action} on {auth.path}")
        return {"status": "ok"} # 200 OK is enough for MediaMTX
    
    print(f"Unauthorized access attempt from IP: {auth.ip}")
    raise HTTPException(status_code=403, detail="Unauthorized")