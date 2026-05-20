from fastapi import APIRouter, HTTPException
from app.schemas.alert import AlertCreate, AlertUpdate
from app.crud.alert import get_alerts, create_alert, update_alert

router = APIRouter(prefix="/alerts")

@router.get("/")
async def read_alerts(camera_id: str | None = None, resolved: bool | None = None, skip: int = 0, limit: int = 50):
    response = get_alerts(camera_id=camera_id, resolved=resolved, skip=skip, limit=limit)
    return response.data

@router.post("/")
async def add_alert(alert: AlertCreate):
    response = create_alert(alert.dict())
    return response.data[0] if response.data else None

@router.patch("/{id}/resolve")
async def resolve_alert(id: str):
    response = update_alert(id, {"resolved": True})
    if not response.data:
        raise HTTPException(status_code=404, detail="Alert not found")
    return response.data[0]

@router.patch("/{id}")
async def edit_alert(id: str, alert: AlertUpdate):
    update_data = {k: v for k, v in alert.dict().items() if v is not None}
    response = update_alert(id, update_data)
    if not response.data:
        raise HTTPException(status_code=404, detail="Alert not found")
    return response.data[0]
