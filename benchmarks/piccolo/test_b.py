import asyncio
import os
import time
from random import choice

from models import Journal, DB

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))
count = int(os.environ.get("ITERATIONS", "1000"))
count = int(count // concurrents) * concurrents


async def _runtest(count):
    async with DB.transaction():
        for i in range(count):
            journal = Journal(level=choice(LEVEL_CHOICE), text=f"Insert from B, item {i}")
            await journal.save()


async def runtest(loopstr):
    start = time.time()
    await asyncio.gather(*[_runtest(count // concurrents) for _ in range(concurrents)])
    now = time.time()
    print(f"Piccolo{loopstr}, B: Rows/sec: {count / (now - start): 10.2f}")
