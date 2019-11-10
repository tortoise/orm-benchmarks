import os
import time
from random import randrange
import asyncio

from models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
iters = int(os.environ.get('ITERATIONS', '1000')) // 2
concurrents = int(os.environ.get('CONCURRENTS', '1'))


async def _runtest(iters) -> int:
    count = 0

    for _ in range(iters):
        for level in LEVEL_CHOICE:
            res = list(await Journal.filter(level=level).limit(20).offset(randrange(int(iters/10))))
            count += len(res)

    return count


async def runtest(loopstr):
    start = now = time.time()
    count = 0

    count = sum(await asyncio.gather(*[_runtest(iters // concurrents) for _ in range(concurrents)]))

    now = time.time()

    print(f'Tortoise ORM{loopstr}, E: Rows/sec: {count / (now - start): 10.2f}')
