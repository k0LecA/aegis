from fastapi import APIRouter
from app.routers import camera, items

router = APIRouter()
router.include_router(camera.router)
router.include_router(items.router)