from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RecordingBase(BaseModel):
    camera_id: str
    file_path: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    size_bytes: Optional[int] = None

class RecordingCreate(RecordingBase):
    pass

class RecordingUpdate(BaseModel):
    camera_id: Optional[str] = None
    file_path: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    size_bytes: Optional[int] = None

class RecordingResponse(RecordingBase):
    id: str
    created_at: datetime
