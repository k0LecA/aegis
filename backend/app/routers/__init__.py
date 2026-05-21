from fastapi import APIRouter
from app.routers import camera, recording, alert, services

router = APIRouter()
router.include_router(camera.router)
router.include_router(recording.router)
router.include_router(alert.router)
router.include_router(services.router)