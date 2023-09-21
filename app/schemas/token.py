from pydantic import BaseModel

from datetime import datetime


class Token(BaseModel):
    exp: datetime
    user_id: str
