#!/usr/bin/env python
import asyncio

import test_a
import test_b
import test_c
import test_d

# import test_e
# import test_f
# import test_g
# import test_h
# import test_i
# import test_j
# import test_k
from models import Base, engine, loopstr


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def run_benchmarks():
    await create_db()
    await test_a.runtest(loopstr)
    await test_b.runtest(loopstr)
    await test_c.runtest(loopstr)
    await test_d.runtest(loopstr)
    # await test_e.runtest(loopstr)
    # await test_f.runtest(loopstr)
    # await test_g.runtest(loopstr)
    # await test_h.runtest(loopstr)
    # await test_i.runtest(loopstr)
    # await test_j.runtest(loopstr)
    # await test_k.runtest(loopstr)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_benchmarks())
