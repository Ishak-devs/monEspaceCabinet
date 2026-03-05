def check_start():

            from pytz import timezone
            paris_tz = timezone("Europe/Paris")
            maintenant = datetime.now(paris_tz).isoformat()

            res = supabase_client.table("prospection_settings")\
                .select("*")\
                .eq("has_run_today", False)\
                .lte("hour_start", maintenant)\
                .execute()

            print(f"CONTENU BRUT SUPABASE : {res.data}")
            data = cast(list[dict[str, Any]], res.data or [])
            print(f"DEBUG - Nombre de jobs trouvés : {len(data)}")
            if any (lock.locked() for lock in user_lock.values()):
                print('lock libéré on vérifie les prospections...')
                time.sleep(60)

            from loop.for_job_in_data import for_job_in_data
            for_job_in_data()
