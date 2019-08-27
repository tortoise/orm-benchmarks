#!/usr/bin/env python
import os
try:
    import os
    concurrents = int(os.environ.get('CONCURRENTS', '1'))

    if concurrents > 1:
        loopstr = f" C{concurrents}"
    else:
        loopstr = ""
    if os.environ.get('UVLOOP', ''):
        import asyncio
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
finally:
    pass


import test_a
import test_b
import test_c
import test_d
import test_e
import test_f
import test_g
import test_h
import test_i
import test_j

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
    await test_c.runtest(loopstr)
    await test_d.runtest(loopstr)
    await test_e.runtest(loopstr)
    await test_f.runtest(loopstr)
    await test_g.runtest(loopstr)
    await test_h.runtest(loopstr)
    await test_i.runtest(loopstr)
    await test_j.runtest(loopstr)


run_async(run_benchmarks())
