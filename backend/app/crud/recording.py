import os
import re
from datetime import datetime, timezone
from app.core.database import supabase

RECORDINGS_DIR = "/home/whiteshark/Projects/aegis/mediamtx/recordings"

def _parse_recording_start_time(filename: str, filepath: str) -> str:
    """Helper to parse started_at ISO timestamp from MediaMTX recording filename."""
    local_tz = datetime.now().astimezone().tzinfo
    
    # Try parsing format with microseconds (%Y-%m-%d_%H-%M-%S_%f)
    match_micro = re.search(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_\d{6})", filename)
    if match_micro:
        try:
            dt = datetime.strptime(match_micro.group(1), "%Y-%m-%d_%H-%M-%S_%f")
            return dt.replace(tzinfo=local_tz).astimezone(timezone.utc).isoformat()
        except ValueError:
            pass

    # Try parsing format without microseconds (%Y-%m-%d_%H-%M-%S)
    match_sec = re.search(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})", filename)
    if match_sec:
        try:
            dt = datetime.strptime(match_sec.group(1), "%Y-%m-%d_%H-%M-%S")
            return dt.replace(tzinfo=local_tz).astimezone(timezone.utc).isoformat()
        except ValueError:
            pass

    # Fallback to file creation timestamp
    return datetime.fromtimestamp(os.path.getctime(filepath), tz=timezone.utc).isoformat()


def sync_local_recordings():
    """Scans the local recordings directory and synchronizes physical mp4 files with Supabase."""
    try:
        # Fetch all cameras from Supabase
        cameras_res = supabase.table("cameras").select("*").execute()
        cameras = cameras_res.data or []
        
        # Create mapping of cleaned directory names to camera records
        camera_map = {}
        for cam in cameras:
            name = cam.get("name", "")
            if name:
                cleaned_name = "".join(c for c in name.lower() if c.isalnum() or c in (" ", "_", "-")).replace(" ", "_")
                camera_map[cleaned_name] = cam
        
        if not os.path.exists(RECORDINGS_DIR):
            return
            
        # Fetch current database records to minimize database queries
        db_recordings_res = supabase.table("recordings").select("*").execute()
        db_recordings = db_recordings_res.data or []
        
        db_by_filepath = {rec["file_path"]: rec for rec in db_recordings}
        scanned_filepaths = set()
        
        # Scan camera-specific subdirectories
        for cleaned_name, camera in camera_map.items():
            cam_dir = os.path.join(RECORDINGS_DIR, cleaned_name)
            if not os.path.isdir(cam_dir):
                continue
                
            for filename in os.listdir(cam_dir):
                if not filename.endswith(".mp4"):
                    continue
                    
                filepath = os.path.abspath(os.path.join(cam_dir, filename))
                scanned_filepaths.add(filepath)
                
                started_at = _parse_recording_start_time(filename, filepath)
                size_bytes = os.path.getsize(filepath)
                mtime = os.path.getmtime(filepath)
                
                # If modified within the last 15 seconds, mark the recording stream as ongoing
                is_active = (datetime.now().timestamp() - mtime) < 15
                ended_at = None if is_active else datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
                
                existing = db_by_filepath.get(filepath)
                if existing:
                    # Update recording details if status or size changed
                    if existing.get("ended_at") != ended_at or existing.get("size_bytes") != size_bytes:
                        supabase.table("recordings").update({
                            "size_bytes": size_bytes,
                            "ended_at": ended_at
                        }).eq("id", existing["id"]).execute()
                else:
                    # Insert a newly found recording record
                    supabase.table("recordings").insert({
                        "camera_id": camera["id"],
                        "file_path": filepath,
                        "started_at": started_at,
                        "ended_at": ended_at,
                        "size_bytes": size_bytes
                    }).execute()
        
        # Clean up database records for physical files that were deleted from disk
        for db_rec in db_recordings:
            db_filepath = db_rec.get("file_path")
            if db_filepath and db_filepath not in scanned_filepaths:
                supabase.table("recordings").delete().eq("id", db_rec["id"]).execute()
                
    except Exception as e:
        print(f"[ERROR] sync_local_recordings failed: {e}")


def get_recordings(camera_id: str | None = None, skip: int = 0, limit: int = 50):
    """Fetch paginated recordings from Supabase after scanning and syncing local files."""
    sync_local_recordings()
    q = supabase.table("recordings").select("*").range(skip, skip + limit - 1)
    if camera_id is not None:
        q = q.eq("camera_id", camera_id)
    return q.execute()

def get_recording(recording_id: str):
    """Fetch a single recording from Supabase by ID."""
    return supabase.table("recordings").select("*").eq("id", recording_id).execute()

def create_recording(data: dict):
    """Insert a new recording record into Supabase."""
    return supabase.table("recordings").insert(data).execute()

def delete_recording(recording_id: str):
    """Delete a recording record from Supabase by ID."""
    return supabase.table("recordings").delete().eq("id", recording_id).execute()
