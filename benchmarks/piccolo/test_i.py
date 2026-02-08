import asyncio
import os
import time
from random import choice

from models import Journal, DB

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(objs) -> int:
    async with DB.transaction():
        for obj in objs:
            obj.level = choice(LEVEL_CHOICE)
            obj.text = f"{obj.text} Update"
            await obj.save()
    return len(objs)


async def runtest(loopstr):
    objs = await Journal.objects()
    inrange = len(objs) // concurrents
    if inrange < 1:
        inrange = 1

    start = time.time()
    count = sum(
        await asyncio.gather(
            *[_runtest(objs[i * inrange : (i + 1) * inrange]) for i in range(concurrents)]
        )
    )
    now = time.time()
    print(f"Piccolo{loopstr}, I: Rows/sec: {count / (now - start): 10.2f}")
