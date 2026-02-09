#!/usr/bin/env python3
"""Generate benchmark charts for ORM comparison."""

import re
import os
import math
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

OPERATION_LABELS = {
    "A": "Insert:\nSingle",
    "B": "Insert:\nBatch",
    "C": "Insert:\nBulk",
    "D": "Filter:\nLarge",
    "E": "Filter:\nSmall",
    "F": "Get",
    "G": "Filter:\ndict",
    "H": "Filter:\ntuple",
    "I": "Update:\nWhole",
    "J": "Update:\nPartial",
    "K": "Delete",
}

ORM_COLORS = {
    "Tortoise ORM": "#2ecc71",
    "Django": "#3498db",
    "peewee": "#e67e22",
    "SA ORM async": "#9b59b6",
    "SQLObject": "#95a5a6",
    "Piccolo": "#e74c3c",
    "ormar": "#1abc9c",
    "SQLModel": "#f39c12",
}

ORM_ORDER = ["Tortoise ORM", "Django", "peewee", "SA ORM async", "SQLObject", "Piccolo", "ormar", "SQLModel"]
OP_ORDER = list("ABCDEFGHIJK")


def parse_results(filepath):
    """Parse benchmark result file into {orm_name: {op: value}}."""
    data = defaultdict(dict)
    with open(filepath) as f:
        for line in f:
            m = re.match(r"^\s*(?:\d+[→\t])?\s*(.+?),\s*([A-K]):\s*Rows/sec:\s*([\d.]+)", line)
            if m:
                orm, op, val = m.group(1).strip(), m.group(2), float(m.group(3))
                data[orm][op] = val
    return dict(data)


def compute_geometric_mean(values):
    """Compute geometric mean of non-zero values."""
    vals = [v for v in values if v > 0]
    if not vals:
        return 0
    return math.exp(sum(math.log(v) for v in vals) / len(vals))


def generate_chart(data, title, output_path, show_geomean=True):
    """Generate a grouped bar chart for benchmark results."""
    orms = [o for o in ORM_ORDER if o in data]
    ops = [o for o in OP_ORDER if any(o in data.get(orm, {}) for orm in orms)]

    n_ops = len(ops) + (1 if show_geomean else 0)
    n_orms = len(orms)
    bar_width = 0.8 / n_orms
    x = np.arange(n_ops)

    fig, ax = plt.subplots(figsize=(max(14, n_ops * 1.5), 7))

    for i, orm in enumerate(orms):
        values = []
        for op in ops:
            values.append(data.get(orm, {}).get(op, 0))
        if show_geomean:
            gm = compute_geometric_mean([v for v in values if v > 0])
            values.append(gm)

        offset = (i - n_orms / 2 + 0.5) * bar_width
        bars = ax.bar(x + offset, values, bar_width * 0.9,
                      label=orm, color=ORM_COLORS.get(orm, "#333"),
                      edgecolor="white", linewidth=0.5, zorder=3)

    labels = [OPERATION_LABELS.get(op, op) for op in ops]
    if show_geomean:
        labels.append("Geometric\nMean")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Rows/sec", fontsize=11, fontweight="bold")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.grid(axis="y", alpha=0.3, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", fontsize=9, ncol=min(n_orms, 4), framealpha=0.9)
    ax.set_xlim(-0.6, n_ops - 0.4)

    if show_geomean:
        ax.axvline(x=n_ops - 1.6, color="#ccc", linestyle="--", linewidth=1, zorder=1)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: {output_path}")


def generate_geomean_summary(all_data, title, output_path):
    """Generate a summary chart comparing geometric means across all tests."""
    test_labels = []
    test_data = {}

    for test_name, data in all_data:
        test_labels.append(test_name)
        for orm, ops in data.items():
            vals = [v for v in ops.values() if v > 0]
            gm = compute_geometric_mean(vals)
            test_data.setdefault(orm, []).append(gm)

    orms = [o for o in ORM_ORDER if o in test_data]
    n_tests = len(test_labels)
    n_orms = len(orms)
    bar_width = 0.8 / n_orms
    x = np.arange(n_tests)

    fig, ax = plt.subplots(figsize=(max(10, n_tests * 3), 6))

    for i, orm in enumerate(orms):
        offset = (i - n_orms / 2 + 0.5) * bar_width
        values = test_data[orm]
        bars = ax.bar(x + offset, values, bar_width * 0.9,
                      label=orm, color=ORM_COLORS.get(orm, "#333"),
                      edgecolor="white", linewidth=0.5, zorder=3)

        for bar, val in zip(bars, values):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        f"{val:,.0f}", ha="center", va="bottom", fontsize=7,
                        fontweight="bold", rotation=45)

    ax.set_xticks(x)
    ax.set_xticklabels(test_labels, fontsize=11, fontweight="bold")
    ax.set_ylabel("Geometric Mean (Rows/sec)", fontsize=11, fontweight="bold")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.grid(axis="y", alpha=0.3, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc="upper right", fontsize=9, ncol=min(n_orms, 4), framealpha=0.9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: {output_path}")


def main():
    base = "/tmp/orm-benchmarks"
    img_dir = os.path.join(base, "images")
    os.makedirs(img_dir, exist_ok=True)

    databases = {
        "pg": {
            "label": "PostgreSQL 17",
            "files": ["/tmp/pg_outfile1", "/tmp/pg_outfile2", "/tmp/pg_outfile3"],
        },
        "mysql": {
            "label": "MySQL 8",
            "files": ["/tmp/mysql_outfile1", "/tmp/mysql_outfile2", "/tmp/mysql_outfile3"],
        },
        "sqlite": {
            "label": "SQLite",
            "files": ["/tmp/sqlite_outfile1", "/tmp/sqlite_outfile2", "/tmp/sqlite_outfile3"],
        },
    }

    test_names = ["Test 1: Simple Model", "Test 2: FK Relations", "Test 3: Wide Model (32+ fields)"]

    for db_key, db_info in databases.items():
        print(f"\n=== {db_info['label']} ===")
        all_tests = []
        for i, (filepath, test_name) in enumerate(zip(db_info["files"], test_names)):
            if not os.path.exists(filepath):
                print(f"  Skipping {filepath} (not found)")
                continue
            data = parse_results(filepath)
            if not data:
                print(f"  Skipping {filepath} (no data)")
                continue
            chart_title = f"{db_info['label']} \u2014 {test_name}"
            output_file = os.path.join(img_dir, f"{db_key}_test{i+1}.png")
            generate_chart(data, chart_title, output_file)
            all_tests.append((test_name, data))

        if all_tests:
            summary_title = f"{db_info['label']} \u2014 Overall (Geometric Mean)"
            summary_file = os.path.join(img_dir, f"{db_key}_summary.png")
            generate_geomean_summary(all_tests, summary_title, summary_file)


if __name__ == "__main__":
    main()
