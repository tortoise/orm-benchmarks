import asyncio
import os
import time

from models import Journal, database

concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(objs) -> int:
    async with database.transaction():
        for obj in objs:
            await obj.delete()
    return len(objs)


async def runtest(loopstr):
    objs = await Journal.objects.all()
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
    print(f"ormar{loopstr}, K: Rows/sec: {count / (now - start): 10.2f}")
