import asyncio
import os
import time

from models import Journal, DB

concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(objs) -> int:
    async with DB.transaction():
        for obj in objs:
            await obj.remove()
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
    print(f"Piccolo{loopstr}, K: Rows/sec: {count / (now - start): 10.2f}")
