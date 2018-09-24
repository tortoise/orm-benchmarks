from tortoise import Tortoise, fields
from tortoise.models import Model


class Journal(Model):
    timestamp = fields.DatetimeField(auto_now_add=True)
    level = fields.SmallIntField(db_index=True)
    text = fields.CharField(max_length=255, db_index=True)


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
