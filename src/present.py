#!/usr/bin/env python
import re
import sys

DESC = {
    'A': 'Insert',
    'B': 'Insert: atomic',
    'C': 'Insert: bulk',
    'D': 'Filter: match',
    'E': 'Filter: contains',
    'F': 'Aggregation',
    'G': 'Cursor efficiency',
}

val = sys.stdin.read()
vals = [text.strip() for text in val.strip().split('\n') if text]

data = {}
tests = set()

for bench in vals:
    orm = bench.split(',')[0].strip()
    test = bench.split(',')[1].split(':')[0].strip()
    ops = bench.split(':')[2].strip()
    data.setdefault(orm, {})[test] = ops
    tests.add(test)

tests = sorted(list(tests))
groups = sorted(data.keys())
titles = [f"-{'':19}"] + [f" {group:11}" for group in groups]

print('')
print(' '.join(['=' * len(text) for text in titles]))
print(' '.join(titles).rstrip())
print(' '.join(['=' * len(text) for text in titles]))

for test in tests:
    results = [f'{DESC[test]:20}']
    for group in groups:
        results.append(f"{data[group].get(test, ''):>11} ")
    print(' '.join(results).rstrip())

print(' '.join(['=' * len(text) for text in titles]))

