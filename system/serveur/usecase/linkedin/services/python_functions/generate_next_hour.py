from datetime import datetime, timedelta
import random

from data.database import supabase_client

def generate_next_hour():
    while True:
        new_hour = (datetime.now().astimezone() + timedelta(days=1)).replace(
            hour=random.randint(8, 19),
            minute=random.randint(0, 59),
            second=0,
            microsecond=0
        )

        check = supabase_client().table("prospection_settings") \
            .select("id") \
            .eq("hour_start", new_hour.isoformat()) \
            .execute()

        if not check.data:
            return new_hour