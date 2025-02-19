from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal

class User(BaseModel):
    email: EmailStr
    firstname: str
    password: str
    created_at: datetime = datetime.now()
    role: Literal["Admin","Client"]