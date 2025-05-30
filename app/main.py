from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(
    title="Book Management API",
    description="API for managing books and users with CRUD operations and search functionality",
    version="1.0.0"
)

# Add CORS middleware - THIS IS THE KEY FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
register_tortoise(
    app,
    db_url="sqlite://app/database/sqlite/db.sqlite3",
    modules={"models": ["app.database.db_models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# Import and include the routers
from app.routes.books import router as books_router
from app.routes.users import router as users_router

app.include_router(books_router)
app.include_router(users_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}