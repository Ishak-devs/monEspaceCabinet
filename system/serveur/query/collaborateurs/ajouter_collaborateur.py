from pathlib import Path

from dotenv import load_dotenv

from data.get_admin_client import get_admin_client
from data.database import supabase_client

def query_ajouter_collaborateur(body):

    try:
            auth_res = get_admin_client().auth.admin.create_user({
                "email": body.email,
                "password": body.password,
            })

            supabase_client().table("profiles").insert({
                "id": auth_res.user.id,
                "email": body.email,
                # "cabinet_id": body.cabinet_id
            }).execute()
    except Exception as e:
            print(f" ERREUR SUPABASE INSERT DANS LA TABLE profiles : {e}")
