import asyncio
import os
import time
from random import randrange

from models import Journal, engine
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

LEVEL_CHOICE = [10, 20, 30, 40, 50]
iters = int(os.environ.get("ITERATIONS", "1000"))
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(_iters):
    count = 0

    async with AsyncSession(engine) as session:
        for _ in range(_iters):
            for level in LEVEL_CHOICE:
                res = list(
                    (
                        await session.execute(
                            select(Journal)
                            .where(Journal.level == level)
                            .limit(20)
                            .offset(randrange(iters - 20))
                        )
                    )
                    .scalars()
                    .all()
                )
                count += len(res)
    return count


async def runtest(loopstr):
    start = now = time.time()
    count = 0

    count = sum(
        await asyncio.gather(
            *[_runtest(iters // 10 // concurrents) for _ in range(concurrents)]
        )
    )

    now = time.time()

    print(f"Async SQLAlchemy ORM{loopstr}, E: Rows/sec: {count / (now - start): 10.2f}")
