import asyncio
import os
import time
from random import choice

from models import Journal, engine
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(objs) -> int:
    async with AsyncSession(engine) as session:
        for obj in objs:
            obj.level = choice(LEVEL_CHOICE)
            session.add(obj)
        await session.commit()

    return len(objs)


async def runtest(loopstr):
    async with AsyncSession(engine) as session:
        objs = list((await session.execute(select(Journal))).scalars().all())
    inrange = len(objs) // concurrents
    if inrange < 1:
        inrange = 1

    start = now = time.time()

    count = sum(
        await asyncio.gather(
            *[
                _runtest(objs[i * inrange : ((i + 1) * inrange) - 1])
                for i in range(concurrents)
            ]
        )
    )

    now = time.time()

    print(f"Async SQLAlchemy ORM{loopstr}, J: Rows/sec: {count / (now - start): 10.2f}")
