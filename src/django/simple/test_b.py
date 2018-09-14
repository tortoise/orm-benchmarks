import django
django.setup()

from simple.models import Journal
import time
from random import choice
import os
from django.db import transaction

LEVEL_CHOICE = [10,20,30,40,50]

count = int(os.environ.get('ITERATIONS', '1000'))
start = now = time.time()
with transaction.atomic():
    for i in range(count):
        Journal.objects.create(
            level = choice(LEVEL_CHOICE),
            text = f'Insert from B, item {i}'
        )
now = time.time()

print(f'Django, B: Rows/sec: {count / (now - start): 10.2f}')

