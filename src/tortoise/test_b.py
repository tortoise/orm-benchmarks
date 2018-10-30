import os
import time
from random import choice

from models import Journal

from tortoise.transactions import in_transaction

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get('ITERATIONS', '1000'))


async def runtest(loopstr):
    start = now = time.time()
    async with in_transaction():
        for i in range(count):
            await Journal.create(
                level=choice(LEVEL_CHOICE),
                text=f'Insert from B, item {i}'
            )
    now = time.time()

    print(f'Tortoise ORM{loopstr}, B: Rows/sec: {count / (now - start): 10.2f}')
