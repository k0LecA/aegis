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

