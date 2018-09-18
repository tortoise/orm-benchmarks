from models import init, runasync
from tortoise import Tortoise

async def create_db():
    # Generate the schema
    await init()
    await Tortoise.generate_schemas()

runasync(create_db())

