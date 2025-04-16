from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from models import Book
from tortoise.exceptions import DoesNotExist

# app = FastAPI()

# @app.get("/Books")
# def get_books():
#     return {"none": "none"}

# @app.get("/Books/{id}")
# def get_books():
#     return {"none": "none"}

# @app.post("/Books")
# def get_books():
#     return {"none": "none"}

# @app.put("/Books/{id}")
# def get_books():
#     return {"none": "none"}

# @app.delete("/Books/{id}")
# def get_books():
#     return {"none": "none"}

# @app.get("/Books/find/{*}")
# def get_books():
#     return {"none": "none"}