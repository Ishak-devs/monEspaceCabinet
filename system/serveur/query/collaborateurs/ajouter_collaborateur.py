from data.database import supabase_client

def ajouter_collaborateur(body, cabinet_id, current_user_id):
        try:
            auth_res = supabase_client().auth.admin.create_user({
                "email": body.intitule,
                "password": body.password,
            })

            supabase_client().table("profiles").insert({
                "id": auth_res.user.id,
                "email": body.intitule,
                "cabinet_id": cabinet_id
            }).execute()
        except Exception as e:
            print(f" ERREUR SUPABASE INSERT DANS LA TABLE users : {e}")
