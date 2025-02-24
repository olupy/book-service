from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import Field
from app.models import Book, User

class UserCreate(BaseModel):
    email: EmailStr
    firstname: str
    password: str
    lastname: str = None

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    firstname: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"



class Borrow(BaseModel):
    book_id: str
    user_id: str
    borrow_date: datetime
    return_date: datetime
    created_at: datetime = Field(default_factory=datetime.now, frozen=True)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True, frozen=True)
    is_returned: bool = Field(default=False, frozen=True)
    is_overdue: bool = Field(default=False, frozen=True)
    book: Optional[Book] = None
    user: Optional[User] = None

    class Config:
        from_attributes = True  # Allows conversion from ORM models