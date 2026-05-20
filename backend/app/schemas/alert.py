from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    camera_id: str
    type: str  # 'motion' | 'intruder'
    resolved: bool = False

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    camera_id: Optional[str] = None
    type: Optional[str] = None
    resolved: Optional[bool] = None

class AlertResponse(AlertBase):
    id: str
    triggered_at: datetime
