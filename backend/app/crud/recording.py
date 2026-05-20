from app.core.database import supabase

def get_recordings(camera_id: str | None = None, skip: int = 0, limit: int = 50):
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
