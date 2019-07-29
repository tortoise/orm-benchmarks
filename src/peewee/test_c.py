import os
import time
from random import choice

from models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
CHUNK_SIZE = 100
count = int(os.environ.get('ITERATIONS', '1000'))

# Work around peewee bulk-insert limitation that is total of 2000 values
test = int(os.environ.get('TEST', '1'))
if test == 3:
    CHUNK_SIZE = 50

chunks = count // CHUNK_SIZE
start = now = time.time()
for _ in range(chunks):
    Journal.insert_many([
        (
            choice(LEVEL_CHOICE),
            f'Insert from C, item {i}'
        ) for i in range(CHUNK_SIZE)
    ], [Journal.level, Journal.text]).execute()
now = time.time()

print(f'peewee, C: Rows/sec: {count / (now - start): 10.2f}')
