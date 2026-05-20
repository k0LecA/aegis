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
        
        path_defaults = data.get("pathDefaults", {})
        if not isinstance(path_defaults, dict):
            path_defaults = {}

        # Extract values favoring pathDefaults first, then fallback to global (deprecated) keys, then hardcoded defaults
        record_val = path_defaults.get("record", data.get("record", False))
        format_val = path_defaults.get("recordFormat", data.get("recordFormat", "fmp4"))
        path_val = path_defaults.get("recordPath", data.get("recordPath", "./recordings/%path/%v_%Y-%m-%d_%H-%M-%S_%f"))
        duration_val = path_defaults.get("recordSegmentDuration", data.get("recordSegmentDuration", "1h"))
        
        # Ensure path_val has required %path placeholder
        if "%path" not in str(path_val):
            path_val = "./recordings/%path/%v_%Y-%m-%d_%H-%M-%S_%f"

        return {
            "record": bool(record_val),
            "recordFormat": str(format_val),
            "recordPath": str(path_val),
            "recordSegmentDuration": str(duration_val)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read config: {str(e)}")

@router.post("/mediamtx/config")
async def save_mediamtx_config(req: ConfigSaveRequest):
    config_path = mediamtx_manager.config_path
    
    # Simple validation for MediaMTX recordPath constraint
    if "%path" not in req.recordPath:
        raise HTTPException(status_code=400, detail="Configuration Error: 'recordPath' template must contain the '%path' placeholder.")

    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {}
        
        # Ensure pathDefaults is present and is a dict
        if "pathDefaults" not in data or not isinstance(data["pathDefaults"], dict):
            data["pathDefaults"] = {}
        
        # Update modernized pathDefaults keys
        data["pathDefaults"]["record"] = req.record
        data["pathDefaults"]["recordFormat"] = req.recordFormat
        data["pathDefaults"]["recordPath"] = req.recordPath
        data["pathDefaults"]["recordSegmentDuration"] = req.recordSegmentDuration
        
        # Remove deprecated root-level keys if they exist
        data.pop("record", None)
        data.pop("recordFormat", None)
        data.pop("recordPath", None)
        data.pop("recordSegmentDuration", None)
        
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
