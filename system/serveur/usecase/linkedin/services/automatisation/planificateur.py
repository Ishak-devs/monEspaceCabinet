import httpx
import asyncio
from supabase import create_client
import os

import logging

from usecase.linkedin.classes.UserRequest import UserRequest
from usecase.linkedin.query.check_start import check_start

logging.basicConfig(filename="planificateur.log", level=logging.info,
                    format='%(asctime)s %(levelname)s %(message)s')

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

async def run():
    res = check_start()
    if res:
        for p in res.data:
            try:
                async with httpx.AsyncClient(timeout=None) as client:
                    await client.post("http://127.0.0.1:8001/backend/linkedin/start_chrome", UserRequest())
                logging.info(p)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    asyncio.run(run())

