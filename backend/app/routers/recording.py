import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.schemas.recording import RecordingCreate
from app.crud.recording import get_recordings, get_recording, create_recording, delete_recording

router = APIRouter(prefix="/recordings")

@router.get("/")
async def read_recordings(camera_id: str | None = None, skip: int = 0, limit: int = 50):
    response = get_recordings(camera_id=camera_id, skip=skip, limit=limit)
    return response.data

@router.get("/{id}")
async def read_recording(id: str):
    response = get_recording(id)
    if not response.data:
        raise HTTPException(status_code=404, detail="Recording not found")
    return response.data[0]

@router.post("/")
async def add_recording(recording: RecordingCreate):
    response = create_recording(recording.dict())
    return response.data[0] if response.data else None

@router.delete("/{id}")
async def remove_recording(id: str):
    # Fetch recording first to get file_path
    record = get_recording(id)
    if not record.data:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    file_path = record.data[0].get("file_path")
    
    # Try deleting database record
    response = delete_recording(id)
    
    # Try safely deleting file from local disk if it exists
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            
    return response.data

@router.get("/{id}/download")
async def download_recording(id: str):
    record = get_recording(id)
    if not record.data:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    file_path = record.data[0].get("file_path")
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Recording file not found on disk")
        
    return FileResponse(file_path, media_type="video/mp4", filename=os.path.basename(file_path))
