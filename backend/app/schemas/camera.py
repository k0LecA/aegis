from pydantic import BaseModel
from typing import Optional

class CameraBase(BaseModel):
    name: str
    rtsp_url: str
    group_id: Optional[str] = None

class CameraCreate(CameraBase):
    pass

class CameraUpdate(BaseModel):
    name: Optional[str] = None
    rtsp_url: Optional[str] = None
    group_id: Optional[str] = None

class CameraResponse(CameraBase):
    id: str