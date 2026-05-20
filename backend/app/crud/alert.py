from app.core.database import supabase

def get_alerts(camera_id: str | None = None, resolved: bool | None = None, skip: int = 0, limit: int = 50):
    q = supabase.table("alerts").select("*").range(skip, skip + limit - 1)
    if camera_id is not None:
        q = q.eq("camera_id", camera_id)
    if resolved is not None:
        q = q.eq("resolved", resolved)
    return q.execute()

def create_alert(data: dict):
    return supabase.table("alerts").insert(data).execute()

def update_alert(alert_id: str, data: dict):
    return supabase.table("alerts").update(data).eq("id", alert_id).execute()
