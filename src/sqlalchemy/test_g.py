import os
import time
from random import randint

from models import Journal, engine
from sqlalchemy.orm import sessionmaker

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get('ITERATIONS', '1000'))
maxval = count - 1
count *= 2


Session = sessionmaker(bind=engine)

start = time.time()
session = Session()

for _ in range(count):
    session.query(Journal).get(randint(1, maxval))

now = time.time()

print(f'SQLAlchemy ORM, G: Rows/sec: {count / (now - start): 10.2f}')
