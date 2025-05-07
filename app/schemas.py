"""
This module contains the base models for the endpoints.
These models are used for request and response validation.
The BookIn model is used for creating and updating books,
while the BookOut model is used for returning book data.
"""

from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

class BookIn(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    status: str

class BookOut(BookIn):
    id: int
    creation_date: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    rol: str = "usuario"
    active: bool = True

class UserCreate(UserBase):
    password: str

    @validator("password")
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v

class UserOut(UserBase):
    id: int
    creation_date: datetime

    class Config:
        from_attributes = True