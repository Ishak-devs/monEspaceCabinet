from fastapi import Depends

from core.app import app
from query.linkedin.get_listes import get_listes
from query.user.get_user_id import get_user_id


@app.get("/backend/prospection/list")
async def root_listes(current_user_id: str = Depends(get_user_id)):
    return get_listes(current_user_id)
