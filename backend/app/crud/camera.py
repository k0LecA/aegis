from supabase import Client
from app.core.database import supabase

def get_cameras():
    return supabase.table("cameras").select("*").execute()

def create_camera(name: str, rtsp_url: str):
    camera_data = {
        "name": name,
        "rtsp_url": rtsp_url
    }
    return supabase.table("cameras").insert(camera_data).execute()

def update_camera(camera_id: str, data: dict):
    return supabase.table("cameras").update(data).eq("id", camera_id).execute()

def delete_camera(camera_id: str):
    return supabase.table("cameras").delete().eq("id", camera_id).execute()

