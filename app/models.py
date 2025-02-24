from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal

class User(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    password: str
    created_at: datetime = datetime.now()
    role: Literal["Admin","Client"]
    is_active: bool = True
    updated_at: datetime = datetime.now()


class Book(BaseModel):
    title: str
    author: str
    publication_date: datetime
    isbn: str
    is_available: bool
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    genre: str
    language: str
    sub_category: str
    publisher: str
    file: str
    cover_image: str


class Borrow(BaseModel):
    book_id: str
    user_id: str
    borrow_date: datetime
    return_date: datetime
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    is_active: bool = True
    is_returned: bool = False
    is_overdue: bool = False
    book: Book
    user: User
