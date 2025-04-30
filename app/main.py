"""
Book Management API

This module implements a REST API for managing books using FastAPI and Tortoise ORM.
"""

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(
    title="Book Management API",
    description="API for managing books with CRUD operations and search functionality",
    version="1.0.0"
)

# Database configuration
register_tortoise(
    app,
    db_url="sqlite://app/database/sqlite/db.sqlite3",
    modules={"models": ["app.database.db_models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# Import and include the books router
from app.routes.books import router as books_router
app.include_router(books_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}