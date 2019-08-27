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

=============== ========== ========== ========== ============== ========== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     6246.34    6582.48    6442.00        2009.32    4268.84     12288.00
Insert: Batch      7535.16    7215.04   23180.62       10679.81    5595.71     17207.25
Insert: Bulk      31288.00   46502.16          —       38682.64          —     46998.06
Filter: Large     72941.55   45770.49  199301.64       73425.85   26947.96    190697.71
Filter: Small     16156.86   26893.54  145468.92       29815.35   31442.98     57863.27
Get                2141.73    3751.80   10366.68        2410.96    6978.96      5839.45
Filter: dict     107850.41   65879.74   96413.80       79192.26          —    298667.56
Filter: tuple    108872.44   65026.41  197668.12      267418.27          —    293165.01
Update: Whole      4112.87    6399.96   21742.46       18912.53   13405.22      6708.60
Update: Partial    4372.91    8399.18   37482.88       29659.51   27308.90      8574.40
Geometric Mean     15469.8   17261.68   44591.67       23530.95   12645.63     35551.09
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     5707.65    6606.12    5364.11        1657.70    4047.87     11845.16
Insert: Batch      8125.22    7621.54   14591.29        8025.45    5465.14     15535.32
Insert: Bulk      34159.80   43504.73          —       39205.77          —     36860.92
Filter: Large     76888.56   40575.91  187698.37       83729.43   26499.38     74453.14
Filter: Small     29921.91   25840.39  139570.42       30680.68   30481.98     41914.24
Get                2951.07    3410.26   10147.93        2459.56    6630.32      5171.71
Filter: dict     112940.73   62776.74   99225.01       85948.95          —    269535.33
Filter: tuple    119613.95   61704.10  188854.35      316671.46          —    263031.29
Update: Whole      4228.92    5088.01   23011.75       11517.34   13609.18      6129.65
Update: Partial    4755.69    8188.28   30805.19       14249.75   27114.53      8449.10
Geometric Mean    17642.96   16224.58   40236.12       20739.27   12345.96     28868.06
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     2820.25    2697.38    3167.20        1517.01    2163.72      5990.40
Insert: Batch      3222.62    2766.16    5314.15        4560.08    2496.23      8384.42
Insert: Bulk       5857.15    7287.97          —       17913.97          —     14414.08
Filter: Large     25186.23   14776.44   50853.61       26430.92   12866.11     16772.37
Filter: Small     13426.07    9837.92   65175.49       12178.56   13661.09     16280.29
Get                1435.19    1126.58    5795.19         975.47    3409.13      2439.10
Filter: dict      31644.01   22808.84   20266.11       21450.59          —     30139.39
Filter: tuple     35223.77   23650.50   49317.79       47879.00          —     31585.85
Update: Whole      2680.54    1459.55   18442.65       14353.99   11925.68      1526.96
Update: Partial    4653.31    7937.40   23125.72       17464.21   23918.42      8019.07
Geometric Mean     7170.21    5950.46   17286.11        10001.8    7115.12      9440.13
=============== ========== ========== ========== ============== ========== ============


PyPy7.1-Py3.6:

=============== ========== ========== ========== ============== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     5291.95    5406.58    6211.32        1099.24      4319.18
Insert: Batch      6483.19    6244.50   19405.61        7404.33     15080.45
Insert: Bulk      17793.08   24278.56          —       21706.66     39388.98
Filter: Large    155024.36   89093.19  364474.56      139338.92     66970.63
Filter: Small      7078.56   70425.88  201122.35       67574.76     46849.88
Get                4421.38    9075.35   10769.43        4566.04      6622.11
Filter: dict     156074.62  132253.55  266586.92      117883.46     89092.91
Filter: tuple    170892.78  140205.22  386376.29      257694.32    120146.14
Geometric Mean    23025.11   31056.81   71762.45       26326.35     29480.96
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     5642.51    5863.88    6428.32        1011.53      5013.79
Insert: Batch      6614.63    7216.42   16667.79        6444.70     21134.26
Insert: Bulk      17552.16   25595.84          —       22214.05     36646.65
Filter: Large    148173.23  106460.99  357077.98      132613.42     65773.03
Filter: Small      6595.42   72073.66  197718.36       57966.06     37938.62
Get                4223.62    8777.45   10059.61        4369.84      7207.34
Filter: dict     150091.11  126328.47  256768.94      117289.25     72180.58
Filter: tuple    171519.92  135989.71  358942.03      245477.56    107071.08
Geometric Mean    22663.89   32527.63   68412.17       24733.65     29276.76
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     2876.04    3233.91    4484.25         861.08      3504.36
Insert: Batch      3383.44    3911.75    8530.83        5482.95     12016.78
Insert: Bulk       5612.00    9189.77          —       16516.97     15898.90
Filter: Large     28642.78   32804.06  144864.05       38558.68      2844.57
Filter: Small      2477.72   26550.13  123077.90       26238.31      2527.95
Get                2484.65    4663.73    7748.91        2584.49      1436.63
Filter: dict      30583.43   42262.39   93946.77       30081.95      2903.30
Filter: tuple     34113.06   48539.72  138695.99       57279.73      9496.52
Geometric Mean     7503.28   13282.29   35341.65       11700.81      4571.34
=============== ========== ========== ========== ============== ============


Quick analysis
--------------
* Pony ORM is heavily optimised for performance, it wins nearly every metric, and often by a large margin.
* Django & SQLAlchemy is surprisingly similar in performance.
* Tortoise ORM is competitive.
* ``Get`` is surprisingly slow for everyone.
* Pony ORM, SQLAlchemy & SQLObject does merge operations for updates, so is technically always partial updates.

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
