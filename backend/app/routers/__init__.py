from fastapi import APIRouter
from app.routers import camera, items, recording, alert

router = APIRouter()
router.include_router(camera.router)
router.include_router(items.router)
router.include_router(recording.router)
router.include_router(alert.router)