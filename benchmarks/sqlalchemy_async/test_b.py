import asyncio
import os
import time
from random import choice

from models import Journal, SessionLocal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))
count = int(os.environ.get("ITERATIONS", "1000"))
count = int(count // concurrents) * concurrents


async def _runtest(count):
    async with SessionLocal() as session:
        for i in range(count):
            session.add(Journal(level=choice(LEVEL_CHOICE), text=f"Insert from B, item {i}"))
        await session.commit()


async def runtest(loopstr):
    start = time.time()
    await asyncio.gather(*[_runtest(count // concurrents) for _ in range(concurrents)])
    now = time.time()
    print(f"SA ORM async{loopstr}, B: Rows/sec: {count / (now - start): 10.2f}")
