from data.database import supabase_client

def insert_url_contactees(url, user_data):
    current_user_id = user_data.get("user_id")
    supabase_client().table("url_contactees").insert(
        {"url": url, "user_id": current_user_id}
    ).execute()