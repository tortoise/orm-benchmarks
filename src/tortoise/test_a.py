import os
import time
from random import choice
import asyncio
from models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get('CONCURRENTS', '1'))
count = int(os.environ.get('ITERATIONS', '1000'))
count = int(count // concurrents) * concurrents


async def _runtest(count):
    for i in range(count):
        await Journal.create(
            level=choice(LEVEL_CHOICE),
            text=f'Insert from A, item {i}'
        )


async def runtest(loopstr):
    start = now = time.time()

    await asyncio.gather(*[_runtest(count // concurrents) for _ in range(concurrents)])

    now = time.time()

    print(f'Tortoise ORM{loopstr}, A: Rows/sec: {count / (now - start): 10.2f}')

