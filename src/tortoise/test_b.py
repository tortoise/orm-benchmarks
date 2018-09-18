from models import Journal, runasync, init
import time
from random import choice
import os
from tortoise.transactions import in_transaction

LEVEL_CHOICE = [10,20,30,40,50]

count = int(os.environ.get('ITERATIONS', '1000'))

async def runtest():
    await init()

    start = now = time.time()
    async with in_transaction():
        for i in range(count):
            await Journal.create(
                level = choice(LEVEL_CHOICE),
                text = f'Insert from B, item {i}'
            )
    now = time.time()

    print(f'Tortoise ORM, B: Rows/sec: {count / (now - start): 10.2f}')

runasync(runtest())
