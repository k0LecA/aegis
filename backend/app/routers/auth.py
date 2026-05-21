import uuid
import re
from typing import Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter()

# Active tokens for frontend-backend auth bridge
active_tokens = set()

# Request schemas
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


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serve the application favicon."""
    return FileResponse("static/favicon.ico")


@router.post("/login")
async def login(req: LoginRequest):
    """Authenticate admin credentials and generate a bridge token."""
    if req.username == "admin" and req.password == "admin":
        token = str(uuid.uuid4())
        active_tokens.add(token)
        print(f"[AUTH] Generated token: {token}")
        return {"token": token}
    raise HTTPException(status_code=401, detail="Subject identification failed.")


@router.post("/auth_check")
async def auth_check(auth: MTXAuthRequest):
    """MediaMTX external authentication hook."""
    # Safely extract any standard UUID present in the query parameters
    query_str = auth.query.strip() if auth.query else ""
    uuid_match = re.search(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", query_str, re.IGNORECASE)
    incoming_token = uuid_match.group(1) if uuid_match else query_str

    if incoming_token in active_tokens:
        return {"status": "ok"}
    
    print(f"[AUTH WARNING] Unauthorized access attempt: token='{incoming_token}', IP={auth.ip}, path={auth.path}")
    raise HTTPException(status_code=403, detail="Unauthorized")
