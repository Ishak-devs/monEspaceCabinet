from data.database import supabase_client
from usecase.linkedin.services.python_functions.generate_next_hour import generate_next_hour


def update_has_run_today_true():
    last_job = (supabase_client().table("prospection_settings").select("id").eq("has_run_today", False)
                .order("id", desc=True).limit(1).execute())

    if last_job.data:
        new_hour = generate_next_hour()
        return (supabase_client().table("prospection_settings").update({"has_run_today": True, "is_active": False,
                                                                        "hour_start": new_hour.isoformat()})
                .eq("id", last_job.data[0]["id"]).execute())