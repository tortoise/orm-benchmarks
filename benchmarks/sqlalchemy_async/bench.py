#!/usr/bin/env python
import asyncio
import os
import sys

try:
    concurrents = int(os.environ.get("CONCURRENTS", "10"))

    if concurrents != 10:
        loopstr = f" C{concurrents}"
    else:
        loopstr = ""
    if os.environ.get("UVLOOP", ""):
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
import test_k
from models import create_tables, engine


async def run_benchmarks():
    await create_tables()
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
    await test_k.runtest(loopstr)
    await engine.dispose()


asyncio.run(run_benchmarks())
