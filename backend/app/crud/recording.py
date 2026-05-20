from app.core.database import supabase
import os
import re
from datetime import datetime, timezone

RECORDINGS_DIR = "/home/whiteshark/Projects/aegis/mediamtx/recordings"

def sync_local_recordings():
    try:
        # 1. Fetch all cameras from Supabase
        cameras_res = supabase.table("cameras").select("*").execute()
        cameras = cameras_res.data if cameras_res.data else []
        
        # Create a mapping from cleaned name to camera dict
        camera_map = {}
        for cam in cameras:
            name = cam.get("name", "")
            if name:
                cleaned_name = "".join(c for c in name.lower() if c.isalnum() or c in (" ", "_", "-")).replace(" ", "_")
                camera_map[cleaned_name] = cam
        
        # 2. Check and scan local recordings directory
        if not os.path.exists(RECORDINGS_DIR):
            return
            
        # Fetch current database records to avoid unnecessary database hits and detect deleted files
        db_recordings_res = supabase.table("recordings").select("*").execute()
        db_recordings = db_recordings_res.data if db_recordings_res.data else []
        
        db_by_filepath = {rec["file_path"]: rec for rec in db_recordings}
        scanned_filepaths = set()
        
        # Loop through each camera subdirectory
        for cleaned_name, camera in camera_map.items():
            cam_dir = os.path.join(RECORDINGS_DIR, cleaned_name)
            if not os.path.isdir(cam_dir):
                continue
                
            for filename in os.listdir(cam_dir):
                if not filename.endswith(".mp4"):
                    continue
                    
                filepath = os.path.abspath(os.path.join(cam_dir, filename))
                scanned_filepaths.add(filepath)
                
                # Parse timestamp from MediaMTX generated filename (e.g. %v_2026-05-20_19-00-58_195829.mp4)
                local_tz = datetime.now().astimezone().tzinfo
                match = re.search(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_\d{6})", filename)
                if match:
                    timestamp_str = match.group(1)
                    try:
                        started_at = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S_%f").replace(tzinfo=local_tz).astimezone(timezone.utc).isoformat()
                    except ValueError:
                        started_at = datetime.fromtimestamp(os.path.getctime(filepath), tz=timezone.utc).isoformat()
                else:
                    match = re.search(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})", filename)
                    if match:
                        timestamp_str = match.group(1)
                        try:
                            started_at = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S").replace(tzinfo=local_tz).astimezone(timezone.utc).isoformat()
                        except ValueError:
                            started_at = datetime.fromtimestamp(os.path.getctime(filepath), tz=timezone.utc).isoformat()
                    else:
                        # Fallback to file creation time
                        started_at = datetime.fromtimestamp(os.path.getctime(filepath), tz=timezone.utc).isoformat()
                
                # Gather size and modification times
                size_bytes = os.path.getsize(filepath)
                mtime = os.path.getmtime(filepath)
                
                # Determine ended_at. If modified in the last 15 seconds, it's considered an active recording stream
                now_ts = datetime.now().timestamp()
                if now_ts - mtime < 15:
                    ended_at = None
                else:
                    ended_at = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
                
                # Update or Insert record
                existing = db_by_filepath.get(filepath)
                if existing:
                    if existing.get("ended_at") != ended_at or existing.get("size_bytes") != size_bytes:
                        supabase.table("recordings").update({
                            "size_bytes": size_bytes,
                            "ended_at": ended_at
                        }).eq("id", existing["id"]).execute()
                else:
                    supabase.table("recordings").insert({
                        "camera_id": camera["id"],
                        "file_path": filepath,
                        "started_at": started_at,
                        "ended_at": ended_at,
                        "size_bytes": size_bytes
                    }).execute()
        
        # 3. Clean up database records that no longer exist physically on disk
        for db_rec in db_recordings:
            db_filepath = db_rec.get("file_path")
            if db_filepath and db_filepath not in scanned_filepaths:
                supabase.table("recordings").delete().eq("id", db_rec["id"]).execute()
                
    except Exception as e:
        print(f"Error in sync_local_recordings: {e}")

def get_recordings(camera_id: str | None = None, skip: int = 0, limit: int = 50):
    sync_local_recordings()
    q = supabase.table("recordings").select("*").range(skip, skip + limit - 1)
    if camera_id is not None:
        q = q.eq("camera_id", camera_id)
    return q.execute()

def get_recording(recording_id: str):
    return supabase.table("recordings").select("*").eq("id", recording_id).execute()

def create_recording(data: dict):
    return supabase.table("recordings").insert(data).execute()

def delete_recording(recording_id: str):
    return supabase.table("recordings").delete().eq("id", recording_id).execute()

