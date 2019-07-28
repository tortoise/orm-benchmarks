#!/usr/bin/env python
import sys
import math


DESC = {
    'A': 'Insert:\xa0Single',
    'B': 'Insert:\xa0Batch',
    'C': 'Insert:\xa0Bulk',
    'D': 'Filter:\xa0Large',
    'E': 'Filter:\xa0Small',
    'F': 'Get',

    'gm': 'Geometric Mean',
}

def geomean(xs):
    return math.exp(math.fsum(math.log(x) for x in xs) / len(xs))

val = sys.stdin.read()
vals = [text.strip() for text in val.strip().split('\n') if text]

data = {}
tests = {'gm'}

for bench in vals:
    orm = bench.split(',')[0].strip()
    test = bench.split(',')[1].split(':')[0].strip()
    ops = bench.split(':')[2].strip()
    data.setdefault(orm, {})[test] = ops
    tests.add(test)

tests = sorted(list(tests))

for group in data.keys():
    gm = float(f"{geomean([float(v) for v in data[group].values()]):.2f}")
    data[group]['gm'] = gm

groups = sorted(data.keys(), key=lambda s: s.lower())
lens = [max(len(text), 10) for text in groups]
titles = [f"{sys.argv[1]:15}"] + [f"{group:{_len}}" for group, _len in zip(groups, lens)]  # noqa

print('')
print(' '.join(['=' * len(text) for text in titles]))
print(' '.join(titles).rstrip())
print(' '.join(['=' * len(text) for text in titles]))

for test in tests:
    results = [f'{DESC[test]:15}']
    for group, _len in zip(groups, lens):
        results.append(f"{data[group].get(test, '—'):>{_len}}")
    print(' '.join(results).rstrip())

print(' '.join(['=' * len(text) for text in titles]))
