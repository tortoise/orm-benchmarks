import asyncio
import os
import time
from random import choice

from models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))
count = int(os.environ.get("ITERATIONS", "1000"))
count = int(count // concurrents) * concurrents


async def _runtest(count):
    await Journal.bulk_create(
        [Journal(level=choice(LEVEL_CHOICE), text=f"Insert from C, item {i}") for i in range(count)]
    )


async def runtest(loopstr):
    start = now = time.time()

    await asyncio.gather(*[_runtest(count // concurrents) for _ in range(concurrents)])

    now = time.time()

    print(f"Tortoise ORM{loopstr}, C: Rows/sec: {count / (now - start): 10.2f}")
