import os
import yaml
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.mediamtx import mediamtx_manager

router = APIRouter(prefix="/services")

class ConfigSaveRequest(BaseModel):
    record: bool
    recordFormat: str
    recordPath: str
    recordSegmentDuration: str

@router.get("/mediamtx/status")
async def get_mediamtx_status():
    return {
        "running": mediamtx_manager.is_running()
    }

@router.post("/mediamtx/toggle")
async def toggle_mediamtx():
    if mediamtx_manager.is_running():
        res = mediamtx_manager.stop()
    else:
        res = mediamtx_manager.start()
    return {
        "running": mediamtx_manager.is_running(),
        "details": res
    }

@router.post("/mediamtx/restart")
async def restart_mediamtx():
    res = mediamtx_manager.restart()
    return {
        "running": mediamtx_manager.is_running(),
        "details": res
    }

@router.get("/mediamtx/config")
async def get_mediamtx_config():
    config_path = mediamtx_manager.config_path
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="MediaMTX config file not found.")
    
    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f) or {}
        
        # Extract individual keys safely
        return {
            "record": bool(data.get("record", False)),
            "recordFormat": str(data.get("recordFormat", "fmp4")),
            "recordPath": str(data.get("recordPath", "./recordings/%v_%Y-%m-%d_%H-%M-%S_%f")),
            "recordSegmentDuration": str(data.get("recordSegmentDuration", "1h"))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read config: {str(e)}")

@router.post("/mediamtx/config")
async def save_mediamtx_config(req: ConfigSaveRequest):
    config_path = mediamtx_manager.config_path
    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {}
        
        # Update designated fields
        data["record"] = req.record
        data["recordFormat"] = req.recordFormat
        data["recordPath"] = req.recordPath
        data["recordSegmentDuration"] = req.recordSegmentDuration
        
        with open(config_path, "w") as f:
            yaml.safe_dump(data, f, default_flow_style=False)
        
        # Immediately re-apply camera paths from Supabase
        mediamtx_manager.sync_cameras()
        
        # If running, restart to apply changes
        if mediamtx_manager.is_running():
            mediamtx_manager.restart()
            
        return {"status": "saved", "running": mediamtx_manager.is_running()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save config: {str(e)}")

@router.get("/mediamtx/logs")
async def get_mediamtx_logs():
    return {
        "logs": mediamtx_manager.get_logs()
    }
