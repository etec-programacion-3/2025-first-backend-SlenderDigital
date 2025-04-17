"""
This module contains the base models for the endpoints.
These models are used for request and response validation.
The BookIn model is used for creating and updating books,
while the BookOut model is used for returning book data.
"""

from pydantic import BaseModel

class BookIn(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    status: str

class BookOut(BookIn):
    id: int
    creation_date: str

    class Config:
        orm_mode = True