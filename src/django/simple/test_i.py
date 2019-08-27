try:
    import django  # noqa
    django.setup()  # noqa
finally:
    pass

import time
from random import choice

from simple.models import Journal
from django.db import transaction

LEVEL_CHOICE = [10, 20, 30, 40, 50]


objs = list(Journal.objects.all())
count = len(objs)

start = time.time()

with transaction.atomic():
    for obj in objs:
        obj.level = choice(LEVEL_CHOICE)
        obj.text = f'{obj.text} Update'
        obj.save()

now = time.time()

print(f'Django, I: Rows/sec: {count / (now - start): 10.2f}')
