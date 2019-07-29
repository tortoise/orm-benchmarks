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

Tests:
------

A. Insert: Single (single entry at a time)
B. Insert: Batch (many batched in a transaction)
C. Insert: Bulk (using bulk insert operations)
D. Filter: Large (a large result set)
E. Filter: Small (a limit 20 with random offset)
F. Get
G. Filter: dict
H. Filter: tuple
I. Update: Whole (update the whole object)
J. Update: Partial (update only a single field of the whole object)


1) Small table, no relations
----------------------------

.. code::

    model Journal:
        id: autonumber primary key
        timestamp: datetime → now()
        level: small int(enum) → 10/20/30/40/50 (indexed)
        text: varchar(255) → A selection of text (indexed)


2) Small table, with relations
------------------------------

.. code::

    model Journal:
        id: autonumber primary key
        timestamp: datetime → now()
        level: small int(enum) → 10/20/30/40/50 (indexed)
        text: varchar(255) → A selection of text (indexed)

        parent: FK to parent BigTree
        child: reverse-FB to parent BigTree
        knows: M2M to BigTree


3) Large table
--------------

.. code::

    model BigTree:
        id: uuid primary key
        created_at: datetime → initial-now()
        updated_at: datetime → always-now()
        level: small int(enum) → 10/20/30/40/50 (indexed)
        text: varchar(255) → A selection of text (indexed)

        # Repeated 2 times with defaults, another 2 times as optional:
        col_float: double
        col_smallint: small integer
        col_int: integer
        col_bigint: big integer
        col_char: char(255)
        col_text: text
        col_decimal: decimal(12,8)
        col_json: json


ORMs:
=====

Django:
        https://www.djangoproject.com/

        Pros:

        * Provides all the essential features
        * Simple, clean, API
        * Great test framework
        * Excellent documentation
        * Migrations done right™

        Cons:

        * Brings whole Django along with it

peewee:
        https://github.com/coleifer/peewee


Pony ORM:
        https://github.com/ponyorm/pony

        Pros:

        * Fast
        * Does cacheing automatically

        Cons:

        * Does not support bulk insert.

SQLAlchemy ORM:
        http://www.sqlalchemy.org/

        Pros:

        * The "de facto" ORM in the python world
        * Supports just about every feature and edge case
        * Documentation re DB quirks is excellent

        Cons:

        * Complicated, layers upon layers of leaky abstractions
        * You have to manage transactions manually
        * You have to write a script to get DDL SQL
        * Documentation expects you to be intimate with SQLAlchemy
        * Migrations are add ons

SQLObject:
        https://github.com/sqlobject/sqlobject

        * Does not support 16-bit integer for ``level``, used 32-bit instead.
        * Does not support bulk insert.

Tortoise ORM:
        https://github.com/tortoise/tortoise-orm

        * Currently the only ``async`` ORM as part of this suite.
        * Disclaimer: I'm an active contributor to this project


Results (SQLite)
================

Results for SQLite, using the ``SHM`` in-memory filesystem on Linux, to try and make the tests more CPU limited, but still do FS round-trips. Also more consistent than an SSD.

Py37:

=============== ========== ========== ========== ============== ========== ============ ===================
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM uvloop
=============== ========== ========== ========== ============== ========== ============ ===================
Insert: Single     5902.96    6729.79    6564.09        1966.68    4388.27      9502.66            13451.39
Insert: Batch      8968.97    7878.45   21587.19       11150.29    5838.65     11563.44            16365.33
Insert: Bulk      36559.00   46980.79          —       41358.64          —     42118.67            42523.49
Filter: Large     78692.53   48608.18  193511.07      109352.06   31111.09    188146.13           185547.35
Filter: Small     30390.64   29010.34  146658.19       33438.96   30142.26     56556.38            62717.91
Get                3117.85    3693.86   10580.70        2729.89    7066.42      4804.15             5731.58
Filter: dict     114025.02   66926.04  110210.53      104402.15          —    284824.97           269132.47
Filter: tuple    117270.27   64482.48  196292.70      301219.73          —    249166.57           260534.66
Geometric Mean    25744.85   22055.54   51185.43       27027.16   11116.79     44991.82            50717.65
=============== ========== ========== ========== ============== ========== ============ ===================

=============== ========== ========== ========== ============== ========== ============ ===================
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM uvloop
=============== ========== ========== ========== ============== ========== ============ ===================
Insert: Single     5791.08    6836.05    5545.92        1701.60    4174.84      8724.74            11790.66
Insert: Batch      8233.39    7665.60   14834.60        8180.82    5363.24      8640.71            13892.06
Insert: Bulk      32232.39   44417.07          —       35292.22          —     35565.14            34493.20
Filter: Large     76745.34   41445.46  182188.36      110694.33   30906.33     94442.62            83646.52
Filter: Small     31186.50   26783.92  141036.40       31477.07   30519.12     41207.13            45078.59
Get                2976.04    3506.07   10162.39        2433.03    6554.99      4102.38             5550.33
Filter: dict     110399.08   61479.14   97916.88       98848.75          —    252362.33           248556.75
Filter: tuple    116082.27   60871.94  173681.86      270774.37          —    245079.33           231620.73
Geometric Mean    24738.73   20714.63   44855.49       24037.95   10672.14      35715.3             40190.4
=============== ========== ========== ========== ============== ========== ============ ===================

=============== ========== ========== ========== ============== ========== ============ ===================
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM uvloop
=============== ========== ========== ========== ============== ========== ============ ===================
Insert: Single     2785.98    2679.04    3122.53        1508.36    2207.47      5467.87             5899.52
Insert: Batch      3142.70    2953.07    5435.05        4798.55    2442.02      6930.99             7695.11
Insert: Bulk       5639.51    7717.35          —       17810.89          —     13519.89            13018.03
Filter: Large     27023.84   15443.11   52896.37       32408.48   14719.62     20613.19            20702.13
Filter: Small     13743.26    9785.87   65430.19       12482.12   13156.73     16321.28            16294.95
Get                1416.11    1191.17    6016.59         969.66    3746.98      2448.24             2120.24
Filter: dict      33871.91   24352.62   21784.59       28137.71          —     34971.98            34456.33
Filter: tuple     38806.95   25551.99   52348.90       49423.66          —     37268.89            36431.95
Geometric Mean      8742.8    7151.13   16956.32        9569.44    5229.67     12375.16            12319.63
=============== ========== ========== ========== ============== ========== ============ ===================

PyPy7.1-Py3.6:

=============== ========== ========== ========== ============== ========== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     5415.72    5613.33    6904.24        1112.58          —      4931.75
Insert: Batch      7167.78    7449.19   19825.62        7382.89          —     21504.18
Insert: Bulk      17715.83   25835.71          —       22498.22          —     40387.83
Filter: Large    156627.29  107906.51  363226.86      141041.60          —     88282.51
Filter: Small      7168.62   73377.52  207428.51       69599.54          —     46738.71
Get                4474.82    8749.60   10057.28        4845.78          —      9668.67
Geometric Mean    12295.52   20528.54   40102.73       14366.04          —     23556.75
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     5591.11    5631.66    6423.44        1027.04          —      4589.07
Insert: Batch      6623.02    7181.15   16900.64        6675.27          —     14295.10
Insert: Bulk      17056.88   25140.69          —       15192.33          —     37646.72
Filter: Large    150158.40  102043.30  366218.65       81213.71          —     65448.46
Filter: Small      6693.76   68008.21  196044.53       58909.49          —     38897.13
Get                4364.26    8532.03   10095.11        4421.60          —      5995.81
Geometric Mean    11851.25   19797.07   37946.82        11407.2          —     18311.22
=============== ========== ========== ========== ============== ========== ============


Quick analysis
--------------
* Pony ORM is heavily optimised for performance, it wins nearly every metric, and often by a large margin.
* Django & SQLAlchemy is surprisingly similar in performance.
* Tortoise ORM is now competitive, especially when using ``uvloop``
* Generally ``uvloop`` provides a modest perf increase.
* ``Get`` is surprisingly slow

PyPy comparison
---------------
* ``peewee`` and ``Pony ORM`` gets a noticeable performance improvement
* ``SQLAlchemy ORM`` is marginally faster
* ``Django`` and ``Tortoise ORM`` is typically slower
* ``SQLObject`` fails


Performance of Tortoise
=======================

Versions
--------

Note that these benchmarks have since changed, so state is not exactly the same as above.
This should only be used as a "guideline" of the improvement in performance since we started with the performance optimization process.

==================== ============== ================ ================ ================ ================ ================ ================
Tortoise ORM:        v0.10.6        v0.10.7          v0.10.8          v0.10.9          v0.10.11         v0.11.3          v0.12.1
-------------------- -------------- ---------------- ---------------- ---------------- ---------------- ---------------- ----------------
Seedup (Insert & Big & Small)         19.4, 1.5, 6.1  25.9, 2.0, 6.6    81.8, 2.2, 8.7  95.3, 2.4, 13.1 118.2, 2.7, 14.6 136.9, 2.4, 13.5
=================================== ================ ================ ================ ================ ================ ================
Insert                        89.89          2180.38          2933.19          7635.42          8297.53          9870.59         14544.81
Insert: atomic               149.59          2481.16          3275.53         11966.53         14791.36         18452.56         18245.26
Insert: bulk                      —                —                —                —                —                —         71124.01
Filter: match              55866.14        101035.06        139482.12        158997.41        165398.56        186298.75        160746.73
Filter: contains           76803.14        100536.06        128669.50        142954.66        167127.12        177623.78        159116.08
Filter: limit 20            4583.53         27830.14         29995.23         39170.17         58740.05         65742.82         60285.42
Get                          233.69          1868.15          2136.20          2818.41          4411.01          4899.04          5208.50
==================== ============== ================ ================ ================ ================ ================ ================

Perf issues identified from profiling
-------------------------------------
* No bulk insert operations
* ``base.executor._field_to_db()`` could be replaced with a pre-computed dict lookup
* ``Model.__init__`` is 72% of large queries, and 28% of small queries
* ``Queryset.resolve_filters`` is doing lots of unnecessary stuff, especially for .get() method
* Get operation is slow (likely slow SQL generation, could be resolved with parametrized query cacheing)


On ``tortoise.models.__init__``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``Model.__init__`` is 72% of large queries, and 28% of small queries

The majority of time is spent doing:

* dynamic kwarg handling control flow
* Defaults
* Type conversion/cleanup: ``field_object.to_python_value(value)``.

An experiment indicate a ~10% speedup by pre-generating a closure lookup for type handlers.

Another experiment indicate a ~20% speedup on by skipping ``field_object.to_python_value(value)``

Another experiment with optimal hand-written code gave a ~90% speedup, but there are several issues wit code-generation:

* Error handling should only be done on parameters that are given
* Can generate a function to call to pass parameters in to
* Can't reliably introspect wether to use to_python_value or not

Taking that into account brings effective speedup down to a less impressive ~50%

On Bulk inserts
^^^^^^^^^^^^^^^
Bulk inserts is noticeably faster if inside a transaction.
We can't safely force a transaction around the entire bulk operation, so leave it as is until we have a safe chunking operation.


On Queryset performance
^^^^^^^^^^^^^^^^^^^^^^^
Since pypika is immutable, and our Queryset object is as well, we need tests to guarantee our immutability.
Then we can aggresively cache querysets.

Also, we can make more queries use parameterised queries, cache SQL generation, and cache prepared queries.

Perf fixes applied
------------------

1) ``aiosqlite`` **polling misalignment** *(sqlite specific)*

   (20-40% speedup for retrieval, **10× — 15×** speedup for insertion): https://github.com/jreese/aiosqlite/pull/12
2) ``pypika`` **improved copy implementation** *(generic)*

   (53% speedup for insertion): https://github.com/kayak/pypika/issues/160
3) ``tortoise.models.__init__`` **restructure** *(generic)*

   (25-30% speedup for retrieval) https://github.com/tortoise/tortoise-orm/pull/51

4) ``tortoise.models.__init__`` **restructure** *(generic)*

   (9-11% speedup for retrieval) https://github.com/tortoise/tortoise-orm/pull/52

5) ``aiosqlite`` **macros** *(sqlite specific)*

   (1-5% speedup for retrieval, 10-40% speedup for insertion) https://github.com/jreese/aiosqlite/pull/13

6) **Simple prepared insert statements** *(generic)*

   (35-250% speedup for insertion) https://github.com/jreese/aiosqlite/pull/13 https://github.com/tortoise/tortoise-orm/pull/54

7) **pre-generate initial pypika query object per model** *(generic)*

   (25-50% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/54

8) **pre-generate filter map, and standard select for all values per model** *(generic)*

   (15-30% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/64

9) **More optimal queryset cloning** *(generic)*

   (6-15% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/64

10) ``pypika`` **improved copy implementation** *(generic)*

    (10-15% speedup for small fetch operations) https://github.com/kayak/pypika/pull/205

11) **Optimised inserts/updates & Bulk create** *(generic)*

    | (5-40% speedup for small insert operations)
    | (350-600% speedup for bulk insert over small insert operations) https://github.com/tortoise/tortoise-orm/pull/142

12) **De-lazied some metadata objects & More efficient queryset manipulation** *(generic)*

    | (15-25% speedup for large fetch operations)
    | (5-30% speedup for small fetches) https://github.com/tortoise/tortoise-orm/pull/158
