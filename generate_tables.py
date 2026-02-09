#!/usr/bin/env python3
"""Generate markdown tables from benchmark results."""

import re
import math
from collections import defaultdict

OP_LABELS = {
    "A": "Insert: Single",
    "B": "Insert: Batch",
    "C": "Insert: Bulk",
    "D": "Filter: Large",
    "E": "Filter: Small",
    "F": "Get",
    "G": "Filter: dict",
    "H": "Filter: tuple",
    "I": "Update: Whole",
    "J": "Update: Partial",
    "K": "Delete",
}

ORM_ORDER = ["Django", "peewee", "SA ORM async", "SQLObject", "Tortoise ORM", "Piccolo", "ormar", "SQLModel"]
OP_ORDER = list("ABCDEFGHIJK")


def parse_results(filepath):
    data = defaultdict(dict)
    with open(filepath) as f:
        for line in f:
            m = re.match(r"^\s*(?:\d+[→\t])?\s*(.+?),\s*([A-K]):\s*Rows/sec:\s*([\d.]+)", line)
            if m:
                orm, op, val = m.group(1).strip(), m.group(2), float(m.group(3))
                data[orm][op] = val
    return dict(data)


def compute_geometric_mean(values):
    vals = [v for v in values if v > 0]
    if not vals:
        return 0
    return math.exp(sum(math.log(v) for v in vals) / len(vals))


def fmt(val):
    if val == 0:
        return "—"
    return f"{val:,.0f}"


def generate_table(data, orms=None):
    if orms is None:
        orms = [o for o in ORM_ORDER if o in data]

    # Find best ORM for each operation
    best = {}
    for op in OP_ORDER:
        max_val = 0
        max_orm = ""
        for orm in orms:
            v = data.get(orm, {}).get(op, 0)
            if v > max_val:
                max_val = v
                max_orm = orm
        best[op] = max_orm

    # Geometric means
    gm = {}
    for orm in orms:
        vals = [data.get(orm, {}).get(op, 0) for op in OP_ORDER]
        gm[orm] = compute_geometric_mean([v for v in vals if v > 0])
    best_gm_orm = max(gm, key=lambda o: gm[o])

    header = "| Operation |" + "|".join(f" {o} " for o in orms) + "| Best |"
    sep = "|-----------|" + "|".join("-" * (len(o) + 2) for o in orms) + "|------|"

    lines = [header, sep]
    for op in OP_ORDER:
        row = f"| {OP_LABELS[op]} |"
        for orm in orms:
            v = data.get(orm, {}).get(op, 0)
            cell = fmt(v)
            if orm == best[op] and v > 0:
                cell = f"**{cell}**"
            row += f" {cell} |"
        row += f" {best[op]} |"
        lines.append(row)

    # Geometric mean row
    row = "| **Geometric Mean** |"
    for orm in orms:
        cell = fmt(gm[orm])
        if orm == best_gm_orm:
            cell = f"**{cell}**"
        row += f" {cell} |"
    row += f" **{best_gm_orm}** |"
    lines.append(row)

    return "\n".join(lines)


# PostgreSQL
print("### PostgreSQL\n")
for i, test_name in enumerate(["Test 1: Simple Model (4 fields)", "Test 2: FK Relations", "Test 3: Wide Model (32+ fields)"], 1):
    data = parse_results(f"/tmp/pg_outfile{i}")
    orms = [o for o in ORM_ORDER if o in data]
    print(f"#### {test_name}\n")
    print(generate_table(data, orms))
    print()

# MySQL
print("\n### MySQL\n")
for i, test_name in enumerate(["Test 1: Simple Model (4 fields)", "Test 2: FK Relations", "Test 3: Wide Model (32+ fields)"], 1):
    data = parse_results(f"/tmp/mysql_outfile{i}")
    orms = [o for o in ORM_ORDER if o in data]
    print(f"#### {test_name}\n")
    print(generate_table(data, orms))
    print()

# SQLite
print("\n### SQLite\n")
for i, test_name in enumerate(["Test 1: Simple Model (4 fields)", "Test 2: FK Relations", "Test 3: Wide Model (32+ fields)"], 1):
    data = parse_results(f"/tmp/sqlite_outfile{i}")
    orms = [o for o in ORM_ORDER if o in data]
    print(f"#### {test_name}\n")
    print(generate_table(data, orms))
    print()
