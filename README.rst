==============
ORM Benchmarks
==============

**Qualification criteria is:**

* Needs to support minimum 2 databases, e.g. sqlite + something-else
* Runs on Python3.7
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
F. Filter with limit 20
G. Get


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

Results for SQLite, using the ``SHM`` in-memory filesystem on Linux, to try and make the tests more CPU limited, but still do FS round-trips. Also more consistent than an SSD.

==================== ========== ========== ========== ============== ========== ============ =====================
\                    Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM (uvloop)
==================== ========== ========== ========== ============== ========== ============ =====================
Insert                  5215.75    5407.97    6466.60        2083.00    3870.31      6988.67               9265.30
Insert: atomic          8556.84    6828.68   24183.37       11708.85    4753.63     10817.68              14704.26
Insert: bulk           32403.06   39708.90          —       45805.25          —            —                     —
Filter: match          73434.87   40110.75  242115.31       96515.65   23233.39    189979.86             185781.73
Filter: contains       80117.92   47144.10  235717.16       89914.74   21471.91    167525.46             177661.70
Filter: limit 20       33787.97   24033.08  399068.56       37986.63   27421.46     56495.16              62932.39
Get                     3161.48    3005.87   11316.85        3116.32    6658.96      3847.30               4781.68
==================== ========== ========== ========== ============== ========== ============ =====================


Quick analysis
--------------
* Pony ORM is heavily optimised for performance, it wins nearly every metric, and often by a large margin.
* Django & SQLAlchemy is surprisingly similar in performance.
* Tortoise ORM is now competitive, especially when using ``uvloop``
* Generally ``uvloop`` provides a modest perf increase.
* ``Get`` is surprisingly slow

Performance of Tortoise
=======================

Versions
--------

==================== ============== ================ ================ ================ ================
Tortoise ORM:        v0.10.6        v0.10.7          v0.10.8          v0.10.9          v0.10.11
-------------------- -------------- ---------------- ---------------- ---------------- ----------------
Seedup (Insert & Big & Small)         19.4, 1.5, 6.1  25.9, 2.0, 6.6    81.8, 2.2, 8.7  95.3, 2.4, 13.1
=================================== ================ ================ ================ ================
Insert                        89.89          2180.38          2933.19          7635.42          8297.53
Insert: atomic               149.59          2481.16          3275.53         11966.53         14791.36
Filter: match              55866.14        101035.06        139482.12        158997.41        165398.56
Filter: contains           76803.14        100536.06        128669.50        142954.66        167127.12
Filter: limit 20            4583.53         27830.14         29995.23         39170.17         58740.05
Get                          233.69          1868.15          2136.20          2818.41          4411.01
==================== ============== ================ ================ ================ ================

Perf issues identified
----------------------
* No bulk insert operations
* Limit filter is much slower than large filters (seems DB limited, except for Pony ORM)
* Get operation is slow (likely slow SQL generation)

On ``tortoise.models.__init__``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The majority of time is spent doing type conversion/cleanup: ``field_object.to_python_value(value)``.
This is something that is correct, so I deem it fine as is, and we don't try to make it run any faster right now.
Besides, we are second fastest for these metrics.

On Queryset performace
^^^^^^^^^^^^^^^^^^^^^^
Since pypika is immutable, and our Queryset object is as well, we need tests to guarantee our immutability.
Then we can aggresively cache querysets.
Also spending a lot of time in _copy.

Also, we can make more queries use parameterised queries, this is a large ``pypika`` undertaking, though.

Perf fixes applied
------------------

1) **``aiosqlite`` polling misalignment** *(sqlite specific)*

   (20-40% speedup for retrieval, **10-15X** speedup for insertion): https://github.com/jreese/aiosqlite/pull/12
2) **``pypika`` improved copy implementation** *(generic)*

   (53% speedup for insertion): https://github.com/kayak/pypika/issues/160
3) **``tortoise.models.__init__`` restructure** *(generic)*

   (25-30% speedup for retrieval) https://github.com/tortoise/tortoise-orm/pull/51

4) **``tortoise.models.__init__`` restructure** *(generic)*

   (9-11% speedup for retrieval) https://github.com/tortoise/tortoise-orm/pull/52

5) **``aiosqlite`` macros** *(sqlite specific)*

   (1-5% speedup for retrieval, 10-40% speedup for insertion) https://github.com/jreese/aiosqlite/pull/13

6) **Simple prepared insert statements** *(generic)*

   (35-250% speedup for insertion) https://github.com/jreese/aiosqlite/pull/13 https://github.com/tortoise/tortoise-orm/pull/54

7) **pre-generate initial pypika query object per model** *(generic)*

   (25-50% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/54

8) **pre-generate filter map, and standard select for all values per model** *(generic)*

   (15-30% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/64

9) **More optimal queryset cloning** *(generic)*

   (6-15% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/64
