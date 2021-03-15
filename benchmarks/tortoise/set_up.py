from models import init
from tortoise import Tortoise, run_async


async def create_db():
    # Generate the schema
    await init()
    await Tortoise.generate_schemas()


run_async(create_db())
