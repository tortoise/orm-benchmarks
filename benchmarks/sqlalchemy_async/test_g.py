import asyncio
import os
import time

from models import Journal, engine
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(inrange) -> int:
    count = 0

    async with AsyncSession(engine) as session:
        for _ in range(inrange):
            for level in LEVEL_CHOICE:
                res = [
                    {k: v for k, v in value.__dict__.items() if k[:4] != "_sa_"}
                    for value in (
                        (
                            await session.execute(
                                select(Journal).where(Journal.level == level)
                            )
                        )
                        .scalars()
                        .all()
                    )
                ]
                count += len(res)

    return count


async def runtest(loopstr):
    inrange = 10 // concurrents
    if inrange < 1:
        inrange = 1

    start = now = time.time()

    count = sum(await asyncio.gather(*[_runtest(inrange) for _ in range(concurrents)]))

    now = time.time()

    print(f"Async SQLAlchemy ORM{loopstr}, G: Rows/sec: {count / (now - start): 10.2f}")
