from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")

    @field_validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError('Username must be alphanumeric')
        return v

class UserCreate(UserBase):
    password: constr(min_length=8, max_length=100)

    @field_validator('password')
    def password_strength(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"[a-z]", v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r"\d", v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[constr(min_length=3, max_length=50)] = None
    password: Optional[constr(min_length=8, max_length=100)] = None

    @field_validator('password')
    def password_strength(cls, v):
        if v is not None:
            if not re.search(r"[A-Z]", v):
                raise ValueError('Password must contain at least one uppercase letter')
            if not re.search(r"[a-z]", v):
                raise ValueError('Password must contain at least one lowercase letter')
            if not re.search(r"\d", v):
                raise ValueError('Password must contain at least one digit')
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
                raise ValueError('Password must contain at least one special character')
        return v

class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 