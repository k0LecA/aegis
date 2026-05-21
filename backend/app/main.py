import uuid
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.core.mediamtx import mediamtx_manager
from app.routers import router

app = FastAPI(title="AEGIS API", description="Automated Enclosure Guardian & Interactive System")

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


@app.on_event("startup")
async def startup_event():
    """Start the MediaMTX subprocess on application startup."""
    mediamtx_manager.start()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the MediaMTX subprocess on application shutdown."""
    mediamtx_manager.stop()


# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# API Routes
app.include_router(router, prefix="/api")

# Static files and favicon serving
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.post("/login")
async def login(req: LoginRequest):
    """Authenticate admin and generate an active bridge token."""
    if req.username == "admin" and req.password == "admin":
        token = str(uuid.uuid4())
        active_tokens.add(token)
        print(f"[AUTH] Generated token: {token}")
        return {"token": token}
    raise HTTPException(status_code=401, detail="Subject identification failed.")


@app.post("/auth_check")
async def auth_check(auth: MTXAuthRequest):
    """MediaMTX external authentication hook."""
    print("--- MediaMTX Authentication Request ---")
    print(f"Payload: {auth.dict()}")
    
    # Extract and clean token from query string (e.g. ?token=...)
    query_str = auth.query.strip() if auth.query else ""
    incoming_token = query_str[6:] if query_str.startswith("token=") else (query_str[5:] if query_str.startswith("?token=") else query_str)
    
    print(f"Extracted token: '{incoming_token}'")
    print(f"Active tokens database: {active_tokens}")

    if incoming_token in active_tokens:
        print("Result: SUCCESS")
        return {"status": "ok"}
    
    print("Result: FAILED - Token unauthorized or expired")
    raise HTTPException(status_code=403, detail="Unauthorized")