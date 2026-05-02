from supabase import Client
from app.core.database import supabase

def get_cameras():
    return supabase.table("cameras").select("*").execute()

def create_camera():
    return supabase.table("cameras").insert(camera_data).execute()

