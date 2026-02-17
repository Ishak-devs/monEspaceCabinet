from database import supabase_client


def get_cabinet_informations(current_user_id, cabinet_id):
    cabinet_id = None
    res_cabinet = (
        supabase_client.table("profiles")
        .select("cabinet_id")
        .eq("id", current_user_id)
        .single()
        .execute()
    )
    res_name = (
        supabase_client.table("cabinets").select("nom").eq("id", cabinet_id).execute()
    )
    if res_cabinet.data and isinstance(res_cabinet.data, dict):
        cabinet_id = res_cabinet.data.get("cabinet_id")

    if res_name.data:
        cabinet_name = res_name.data.get("nom", "")
        print(f"✅ Nom du cabinet récupéré : {cabinet_name}")

        print(f"ID du cabinet récupéré : {cabinet_id}")

    print("On lance la requête")

    return cabinet_id
