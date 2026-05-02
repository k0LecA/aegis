from fastapi import APIRouter, Depends
from app.schemas.camera import CameraCreate
from app.crud.camera import get_cameras, create_camera

router = APIRouter(prefix="/cameras")

@router.get("/")
async def read_cameras():
    response = get_cameras() 
    return response.data