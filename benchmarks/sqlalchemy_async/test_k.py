import asyncio
import os
import time

from sqlalchemy import select
from models import Journal, SessionLocal

concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(objs) -> int:
    async with SessionLocal() as session:
        for obj in objs:
            merged = await session.merge(obj)
            await session.delete(merged)
        await session.commit()
    return len(objs)


async def runtest(loopstr):
    async with SessionLocal() as session:
        result = await session.execute(select(Journal))
        objs = result.scalars().all()

    count_obj = len(objs)
    inrange = count_obj // concurrents
    if inrange < 1:
        inrange = 1

    start = time.time()
    count = sum(
        await asyncio.gather(
            *[_runtest(objs[i * inrange : ((i + 1) * inrange)]) for i in range(concurrents)]
        )
    )
    now = time.time()
    print(f"SA ORM async{loopstr}, K: Rows/sec: {count / (now - start): 10.2f}")
