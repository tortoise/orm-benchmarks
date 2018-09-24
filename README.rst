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

Interesting Profiling results
-----------------------------

**test_b**:
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
* Transactioned inserts appear to be much slower than expected, at about an order of magnitude behind Pony ORM.
* ``pypika`` calls deepcopy too agressively in ``pypika/utils.py:44``
* ``tortoise.models.__init__`` → investigate

On ``pypika`` deepcopy use
^^^^^^^^^^^^^^^^^^^^^^^^^^

Replacing the deepcopy() in _copy with a copy() results in::

  Tortoise ORM, A: Rows/sec:    1252.81
  Tortoise ORM, B: Rows/sec:    4339.90

Which is a significant speedup (28% and 83%). Which makes one think, why is deepcopy() used?Is our own query builder class suceptible to the same reference-instead-of-copy that Python monoids often are? Is there a way to avoid the common case of using pypika for saving/inserting?
I think to answer these questions, we need to have tests for checking modification of the monoid, and our suceptibility thereof. And an investigation re the common case of module saving.

Perf fixes applied
------------------

* ``aiosqlite`` polling misalignment: https://github.com/jreese/aiosqlite/pull/12
