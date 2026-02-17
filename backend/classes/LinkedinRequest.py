from typing import Optional

from pydantic import BaseModel


class LinkedinRequest(BaseModel):  # contrat
    intitule: str
    mode: str
    details: str
    telephone: str
    full_name: str
    offre: Optional[str] = None
    post: Optional[str] = None
