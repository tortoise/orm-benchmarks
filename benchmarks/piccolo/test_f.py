import asyncio
import os
import time
from random import randint

from models import Journal

concurrents = int(os.environ.get("CONCURRENTS", "10"))
count = int(os.environ.get("ITERATIONS", "1000"))
maxval = count - 1
count *= 2


async def _runtest(count):
    for _ in range(count):
        await Journal.objects().where(Journal.id == randint(1, maxval)).first()


async def runtest(loopstr):
    start = time.time()
    await asyncio.gather(*[_runtest(count // concurrents) for _ in range(concurrents)])
    now = time.time()
    print(f"Piccolo{loopstr}, F: Rows/sec: {count / (now - start): 10.2f}")
