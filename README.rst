==============
ORM Benchmarks
==============

**Qualification criteria is:**

* Needs to support minimum 2 databases, e.g. sqlite + something-else
* Runs on Python3.6
* Actively developed
* Has ability to generate initial DDL off specified models
* Handle one-to-many relationships


Benchmarks:
===========

These benchmarks are not meant to be used as a direct comparison.
They suffer from co-operative back-off, and is a lot simpler than common real-world scenarios.

1) Single table
---------------

.. code::

    model Journal:
        timestamp: datetime → now()
        level: int(enum) → 10/20/30/40/50
        text: varchar(255) → A selection of text

A. Insert rows (naïve implementation)
B. Insert rows (transactioned)
C. Inster rows (batch)
D. Filter on level
E. Search in text
F. Aggregation
G. Cursor efficiency


2) Relational
-------------
TODO



ORMs:
=====

Django:
        https://www.djangoproject.com/

peewee:
        https://github.com/coleifer/peewee

Pony ORM:
        https://github.com/ponyorm/pony

        * Does not support bulk insert.

SQLAlchemy ORM:
        http://www.sqlalchemy.org/

SQLObject:
        https://github.com/sqlobject/sqlobject

        * Does not support 16-bit integer for ``level``, used 32-bit instead.
        * Does not support bulk insert.

Tortoise ORM:
        https://github.com/tortoise/tortoise-orm

        * Currently the only ``async`` ORM as part of this suite.
        * Does not support bulk insert.

Results (SQLite)
================

==================== ============== ============== ============== ============== ============== ==============
\                    Django         peewee         Pony ORM       SQLAlchemy ORM SQLObject      Tortoise ORM
==================== ============== ============== ============== ============== ============== ==============
Insert                      1103.21        1162.59        1824.69        1027.65        1388.52         977.47
Insert: atomic              7528.52        6251.02       22635.28       11298.14        4836.22        2362.94
Insert: bulk               24251.32       15010.20              —       42748.38              —              —
Filter: match              58217.95       37746.84      232541.34       93751.77       23456.15      110509.19
Filter: contains           58496.86       37138.48      237618.71       88206.71       21451.85      111521.11
==================== ============== ============== ============== ============== ============== ==============


Performance of Tortoise
=======================

Profiling
---------

**test_a**:
    Potential upper bound could be ~3k ops

    ====== ============== =======================================
    Time % function       At
    ====== ============== =======================================
    73.04% execute_insert tortoise/backends/sqlite/executor.py:32
    44.62% _copy          pypika/utils.py:44
    39.92% deepcopy       copy.py:132
    16.15% execute_query  tortoise/backends/sqlite/client:54
    7.06%  __str__        pypika/queries.py:630
    ====== ============== =======================================

**test_b**:
    Potential upper bound could be ~10kops

    ====== ============== =======================================
    Time % function       At
    ====== ============== =======================================
    92.06% execute_insert tortoise/backends/sqlite/executor.py:32
    60.81% _copy          pypika/utils.py:44
    55.16% deepcopy       copy.py:132
    18.22% execute_query  tortoise/backends/sqlite/client:54
    7.71%  __str__        pypika/queries.py:630
    ====== ============== =======================================

**test_d**:
    Potential upper bound could be ~1200kops

    ====== ============== =======================================
    Time % function       At
    ====== ============== =======================================
    92.06% execute_select tortoise/backends/sqlite/executor.py:18
    81.27% __init__       tortoise/models.py:329
    7.48%  execute_query  tortoise/backends/sqlite/client:54
    ====== ============== =======================================

Perf issues identified
----------------------
* No bulk insert operations
* ``aiosqlite`` runs sqlite in a separate thread, so has thread syncronisation costs. It is vastly better from version 0.6.0, but evidently still there.
* Transactioned inserts appear to be much slower than expected, at about an order of magnitude behind Pony ORM.
* ``pypika`` calls deepcopy too agressively in ``pypika/utils.py:44``
* ``tortoise.models.__init__`` → investigate
