import httpx
import asyncio
import os
import logging
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace("/usecase/linkedin/services/automatisation", ""))


from data.database import supabase_client

from usecase.linkedin.classes.UserRequest import UserRequest
from usecase.linkedin.query.check_start import check_start

logging.basicConfig(filename="planificateur.log", level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

supabase = supabase_client()

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

