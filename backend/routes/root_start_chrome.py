from fastapi import Depends

from classes.UserRequest import  UserRequest
from core.app import app, KEY_SECRET
from generate_next_hour import generatehour
from query.cabinets.get_cabinet_id import get_cabinet_id
from query.cabinets.insert_prospection_settings import insert_prospection_settings
from query.user.get_user_id import get_user_id


def get_cabinet_informations(current_user_id, cabinet_id):
    pass


@app.post("/backend/linkedin/start_chrome")
async def root_start_chrome(
    body: UserRequest,
    current_user_id: str = Depends(get_user_id),
    cabinet_id: str = Depends(get_cabinet_id),
):

    get_cabinet_informations(current_user_id, cabinet_id)

    SELECT_QUERY = f"*,profiles!inner(linkedin_email,linkedin_password:pgp_sym_decrypt(linkedin_password::bytea,'{KEY_SECRET}'))"
    if SELECT_QUERY:
        print("insert db...")

    generate_next_hour = generatehour()

    insert_prospection_settings(body, cabinet_id, current_user_id, generate_next_hour)
