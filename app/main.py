from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from app.models import Book
from tortoise.exceptions import DoesNotExist
from models import BookIn, BookOut

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}