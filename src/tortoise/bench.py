#!/usr/bin/env python
try:
    import os

    loopstr = ''
    if os.environ.get('UVLOOP', ''):
        import asyncio
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loopstr = ' (uvloop)'
finally:
    pass

import test_a
import test_b
import test_d
import test_e
import test_f
import test_g

from tortoise import Tortoise, run_async


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite:///dev/shm/db.sqlite3',
        modules={'models': ['models']}
    )


async def create_db():
    # Generate the schema
    await init()
    await Tortoise.generate_schemas()


async def run_benchmarks():
    await create_db()
    await test_a.runtest(loopstr)
    await test_b.runtest(loopstr)
    await test_d.runtest(loopstr)
    await test_e.runtest(loopstr)
    await test_f.runtest(loopstr)
    await test_g.runtest(loopstr)


run_async(run_benchmarks())
