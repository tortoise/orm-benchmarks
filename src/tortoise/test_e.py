import time
import os
from models import Journal
import asyncio

concurrents = int(os.environ.get('CONCURRENTS', '1'))


async def _runtest(inrange) -> int:
    count = 0

    for _ in range(inrange):
        for level in ['A', 'B', 'C']:
            res = list(await Journal.filter(text__contains=f'from {level},').all())
            count += len(res)

    return count


async def runtest(loopstr):
    inrange = 10 // concurrents
    if inrange < 1:
        inrange = 1

    start = now = time.time()

    count = sum(await asyncio.gather(*[_runtest(inrange) for _ in range(concurrents)]))

    now = time.time()

    print(f'Tortoise ORM{loopstr}, E: Rows/sec: {count / (now - start): 10.2f}')
