from fastapi import APIRouter, Depends
from app.schemas.camera import CameraCreate, CameraUpdate
from app.crud.camera import get_cameras, create_camera, update_camera, delete_camera
from app.core.mediamtx import mediamtx_manager

router = APIRouter(prefix="/cameras")

@router.get("/")
async def read_cameras():
    response = get_cameras() 
    return response.data

@router.post("/")
async def add_camera(camera: CameraCreate):
    response = create_camera(camera.name, camera.rtsp_url)
    mediamtx_manager.sync_cameras()
    return response.data

@router.put("/{id}")
async def edit_camera(id: str, camera: CameraUpdate):
    update_data = {k: v for k, v in camera.dict().items() if v is not None}
    response = update_camera(id, update_data)
    mediamtx_manager.sync_cameras()
    return response.data

@router.delete("/{id}")
async def remove_camera(id: str):
    response = delete_camera(id)
    mediamtx_manager.sync_cameras()
    return response.data