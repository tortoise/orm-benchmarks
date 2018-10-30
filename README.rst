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
Insert                  4980.95    5045.09    6248.03        1845.74    3665.67      5792.54               7918.78
Insert: atomic          8708.52    7167.83   24410.57       10462.22    4785.33      9503.29              14617.72
Insert: bulk           33074.79   36294.24          —       38256.39          —            —                     —
Filter: match          72155.73   42314.92  225353.25       85566.52   22437.40    162902.83             164817.51
Filter: contains       72412.91   42792.44  225881.36       79792.05   19566.61    171520.22             159837.96
Filter: limit 20       31142.74   26337.39  359444.32       35385.71   24940.91     38700.04              43038.83
Get                     2823.60    3404.14    9964.79        2903.34    6182.48      2449.86               2838.41
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

(benchmarks changed, so the below is not directly comparable to above)

==================== ============== ================ ================ ================
Tortoise ORM:        v0.10.6        v0.10.7          v0.10.8          v0.10.9
-------------------- -------------- ---------------- ---------------- ----------------
Seedup (Insert & Filter & Get)        12.8, 1.5, 5.0  18.2, 2.2, 10.6  68.6, 2.4, 14.8
=================================== ================ ================ ================
Insert                        94.54           977.47          1168.51          2062.60
Insert: atomic               143.16          2362.94          3434.66         14254.19
Filter: match              67100.22        110509.19        156315.69        169346.58
Filter: contains           80936.28        111521.11        158048.75        163696.72
Filter: limit 20            5091.39         16088.49         32457.13         40244.54
Get                          204.72          1022.30          2176.81          3020.30
==================== ============== ================ ================ ================

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
