import asyncio
import os
import time

from sqlalchemy import select
from models import Journal, SessionLocal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(inrange) -> int:
    count = 0
    async with SessionLocal() as session:
        for _ in range(inrange):
            for level in LEVEL_CHOICE:
                result = await session.execute(select(Journal).where(Journal.level == level))
                res = result.scalars().all()
                count += len(res)
    return count


async def runtest(loopstr):
    inrange = 10 // concurrents
    if inrange < 1:
        inrange = 1

    start = time.time()
    count = sum(await asyncio.gather(*[_runtest(inrange) for _ in range(concurrents)]))
    now = time.time()
    print(f"SA ORM async{loopstr}, D: Rows/sec: {count / (now - start): 10.2f}")
