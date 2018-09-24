import os
import time
from random import choice

from models import Journal, engine
from sqlalchemy.orm import sessionmaker

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get('ITERATIONS', '1000'))


Session = sessionmaker(bind=engine)
start = now = time.time()
session = Session()
for i in range(count):
    session.add(Journal(
        level=choice(LEVEL_CHOICE),
        text=f'Insert from A, item {i}'
    ))
    session.commit()
now = time.time()

print(f'SQLAlchemy ORM, A: Rows/sec: {count / (now - start): 10.2f}')
