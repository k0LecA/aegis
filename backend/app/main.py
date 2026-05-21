from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import router
from app.routers.auth import router as auth_router, verify_token

app = FastAPI(title="AEGIS API", description="Automated Enclosure Guardian & Interactive System")

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Application Routes
app.include_router(router, prefix="/api", dependencies=[Depends(verify_token)])  # Secure database and camera configurations
app.include_router(auth_router)                                                 # Public auth interfaces and hooks

# Static files mount
app.mount("/static", StaticFiles(directory="static"), name="static")