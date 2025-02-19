from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    firstname: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    firstname: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"