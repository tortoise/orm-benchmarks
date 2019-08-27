import time
import os
from models import Journal
import asyncio
from random import choice
from tortoise.transactions import in_transaction


LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get('CONCURRENTS', '1'))

async def runtest(loopstr):
    inrange = 10 // concurrents
    if inrange < 1:
        inrange = 1

    objs = list(await Journal.all())
    count = len(objs)

    start = now = time.time()

    async with in_transaction():
        for obj in objs:
            await obj.delete()

    now = time.time()

    print(f'Tortoise ORM{loopstr}, K: Rows/sec: {count / (now - start): 10.2f}')
