from pydantic import BaseModel
from typing import Optional

class CameraBase(BaseModel):
    name: str
    rtsp_url: str
    group_id: Optional[str] = None

class CameraCreate(CameraBase):
    pass

class CameraResponse(CameraBase):
    id: str