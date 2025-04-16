from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["models"]}  # This tells Tortoise where your models.py is
    )
    await Tortoise.generate_schemas()