import asyncio
from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url="sqlite://app/database/sqlite/db.sqlite3",
        modules={"models": ["app.database.db_models"]}  # Point to your models.py
    )
    await Tortoise.generate_schemas()
    print("Database initialized successfully!")

if __name__ == "__main__":
    print("Initializing database...")
    asyncio.run(init_db())
