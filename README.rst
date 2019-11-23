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
K. Delete


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
Insert: Single     4430.01    6520.70    6396.36        1993.30    4292.23     12070.46
Insert: Batch      8909.67    7330.32   21422.04       10402.52    5223.19     15694.59
Insert: Bulk      38281.25   41996.75          —       35030.01          —    107555.36
Filter: Large     75818.53   44284.75  192368.82       81664.71   26253.58    238029.26
Filter: Small     29598.22   28262.04  138055.70       32218.56   31159.10     59414.85
Get                3146.37    3728.43   10103.97        2697.35    6860.23      5615.90
Filter: dict     109146.11   63681.61  106100.57       81882.96          —    335593.63
Filter: tuple    119365.89   61195.28  191543.08      334111.92          —    304179.15
Update: Whole      4532.25    6318.83   24832.15       19386.39   12814.07     19790.94
Update: Partial    5060.87    8162.99   35747.18       27895.32   25837.39     22102.74
Delete             5697.61   12137.29   52677.07       51684.59    5360.79     24618.34
Geometric Mean    16046.63   16385.16   45116.32       26169.25   11056.35     45614.81
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     5840.00    6260.64    5177.39        1657.84    4090.74     10221.64
Insert: Batch      7853.33    7366.69   13623.51        7851.06    5360.58     13999.52
Insert: Bulk      31776.11   43252.91          —       37703.30          —     83845.50
Filter: Large     73821.40   39419.35  178331.98       76104.42   25730.99    214720.04
Filter: Small     29133.59   25178.73  134017.38       30380.95   29558.21     55342.96
Get                2932.99    3360.05   10024.25        2442.60    6575.97      5637.94
Filter: dict     108454.07   58629.54   95677.76       79256.64          —    274749.21
Filter: tuple    113159.22   58785.24  179365.68      302098.84          —    269286.26
Update: Whole      4210.05    5599.37   22631.96       10858.13   13440.83     18282.56
Update: Partial    4798.56    8009.31   29897.51       13343.75   26376.61     22073.60
Delete              894.07   12139.75   24811.09         536.21    3650.33     24101.28
Geometric Mean    13152.69   15508.68   37045.85       14310.69   10447.46     41186.21
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     2857.47    3053.95    2981.42        1574.60    2200.07      4404.31
Insert: Batch      3205.23    3202.46    4856.01        4861.68    2426.41      8069.06
Insert: Bulk       5828.94    9693.88          —       17063.99          —     17505.83
Filter: Large     24237.35   14151.86   48704.61       26136.00   12427.48     24294.60
Filter: Small     12770.96    9264.17   62728.40       12225.35   13619.54     18691.78
Get                1424.23    1136.20    5437.41         948.11    3633.92      2260.19
Filter: dict      30456.13   21823.94   19688.42       20257.60          —     27934.01
Filter: tuple     33590.00   22951.61   48404.56       44468.98          —     28575.15
Update: Whole      2667.50    1494.76   17710.87       13528.63   11682.46      9735.00
Update: Partial    4620.34    8100.54   22788.73       15951.24   23252.16     21770.90
Delete             5538.67   11964.15   39302.58       30302.47    3400.64     24891.37
Geometric Mean     6883.33    6593.99    18032.7       10799.79    6460.04     13488.42
=============== ========== ========== ========== ============== ========== ============


PyPy7.2-Py3.6:

=============== ========== ========== ========== ============== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     4844.65    5699.46    6069.36         928.29      4119.27
Insert: Batch      6623.80    5942.15   14888.52        6750.90     19889.84
Insert: Bulk      15833.01   19876.12          —       19456.28     59792.55
Filter: Large    145843.64   96627.96  212065.79      110034.60     83070.61
Filter: Small      4867.78   61654.60  172243.99       56155.40     40043.36
Get                3538.23    7448.17    5911.03        4175.23      8464.85
Filter: dict     142764.62  109864.27  131992.03      121185.63     94067.34
Filter: tuple    143723.62  106352.47  206592.66      263009.74    126491.99
Update: Whole      6448.56   14572.05   19806.92       23459.62     25520.65
Update: Partial    7320.68   20191.26   32069.98       40098.96     36326.02
Delete             8583.36   29682.59   73035.62       83364.88     37541.98
Geometric Mean    15281.28   25564.53   43575.11       27864.52     33369.34
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     4856.53    6099.71    6302.97         886.47      4709.30
Insert: Batch      6388.57    5979.01   14255.97        4636.63     19616.08
Insert: Bulk      15675.79   18751.54          —       17444.69     62711.06
Filter: Large    130201.72   86533.17  311024.40      110243.82     69154.04
Filter: Small      3845.09   65312.52  183754.86       47955.16     36348.92
Get                3540.29    7934.10    9121.36        4233.04      6100.74
Filter: dict     138333.47  105259.77  237840.16      119919.30     77601.55
Filter: tuple    155187.72   89280.79  335520.30      260503.32    116994.87
Update: Whole      6693.48   13079.63   37170.20       18749.98     22658.09
Update: Partial    7609.05   17583.81   47285.79       27172.58     35797.50
Delete             2339.78   36752.54   41859.66         655.36     40024.90
Geometric Mean    13247.47   25048.86    55454.4       15927.71     31084.92
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     1965.02    3519.71    4207.43         670.29      3592.01
Insert: Batch      1904.72    3493.31    7636.38        4421.69     12099.74
Insert: Bulk       4054.34    7156.34          —       13786.11     24692.28
Filter: Large     20301.33   29613.15  122365.02       38721.68      2855.62
Filter: Small      1908.01   26244.67  105406.30       24031.37      2478.21
Get                2111.95    4936.50    6633.01        2315.14      1348.12
Filter: dict      28415.33   39443.07   75871.80       28089.40      2995.77
Filter: tuple     26695.73   39080.83  125314.67       58677.38     10422.97
Update: Whole      4072.91    5559.29   27090.75       11341.40     12903.72
Update: Partial    7782.08   20601.30   37512.08       14907.51     31801.49
Delete             9303.80   26078.32   59424.56       63702.66     42910.38
Geometric Mean     5855.94   12832.73   33099.23       12839.01      7698.50
=============== ========== ========== ========== ============== ============

Results (PostgreSQL)
====================

PostgreSQL 11.4 on my notebook.

=============== ========== ========== ========== ============== ========== ============ ================
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     4378.75    3082.51    3750.11        2157.78    3696.39      4295.10          8012.22
Insert: Batch      4503.50    3372.84    7642.85        3812.09    3402.84     11999.09         16619.99
Insert: Bulk      22992.31   25863.10          —       11825.37          —     22558.06         57351.81
Filter: Large    172074.60  107346.86  301376.00       90543.96   49210.84    305500.06        278808.75
Filter: Small     30854.54   19673.55  153697.64       24568.97   28800.75     14862.96         55180.57
Get                2869.67    2611.87    7227.55        2009.65    6249.46      1521.70          3443.29
Filter: dict     470236.12  222537.00  134576.20       90009.27          —    601531.40        519428.32
Filter: tuple    644380.36  217394.55  287233.39      393938.51          —    476092.02        424539.88
Update: Whole      2917.96    3713.08    8133.06        6896.37    5062.30     12534.81         12259.33
Update: Partial    3197.47    4679.77    9782.70       11411.44   10077.58     12973.47         11885.85
Delete             3835.95    7452.18   13489.02       15014.02    4782.40     17587.49         17183.62
Geometric Mean    18252.58   15097.95   28840.07       16051.01    8497.37     27416.87         37773.45
=============== ========== ========== ========== ============== ========== ============ ================

=============== ========== ========== ========== ============== ========== ============ ================
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     4090.74    3112.24    3552.15        1762.13    3408.60      2357.23          7660.13
Insert: Batch      4391.07    3342.24    6665.99        4377.59    3173.67     10905.18         16220.11
Insert: Bulk      19488.62   24360.04          —       11607.94          —     21021.58         53477.43
Filter: Large    169320.84   89343.55  267918.48       87232.49   46630.21    279724.95        257705.45
Filter: Small     28336.64   25904.44  149893.21       19984.76   42485.16     14875.73         54949.07
Get                2729.51    2348.99    6974.78        1856.18    5908.93      1707.68          3309.87
Filter: dict     482952.87  194139.49  116790.05       84609.78          —    556625.88        508470.54
Filter: tuple    641175.00  194788.43  270252.59      371647.44          —    431772.47        400993.01
Update: Whole      2774.30    3383.19    7956.60        5703.26    5154.07     10994.98         11107.63
Update: Partial    3157.57    4588.59    9794.43        8090.78   10076.74      9595.47         12160.01
Delete              666.79    6142.85    8214.61         262.47     745.05       809.87           768.03
Geometric Mean    14942.56   14262.52   25865.09       10089.93    6859.24     18337.77         27419.71
=============== ========== ========== ========== ============== ========== ============ ================

=============== ========== ========== ========== ============== ========== ============ ================
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     1758.27    1518.14    1832.50        1277.21    1566.39      2294.95          5449.79
Insert: Batch      1823.14    1684.99    2135.76        1603.96    1631.35      6650.08          9405.08
Insert: Bulk       3386.76    6721.14          —        5940.08          —     10417.64         17973.64
Filter: Large     34446.74   19443.61   56139.10       29370.45   17762.98     37052.88         28545.87
Filter: Small     14304.19    9653.08   65000.12       10742.42   14042.78      8569.48         21397.55
Get                1313.94     889.92    3770.34         792.37    3077.81       834.98          2171.90
Filter: dict      44473.56   36114.31   21119.13       24100.89          —     57860.90         39383.58
Filter: tuple     51395.38   39045.68   56280.44       52996.84          —     46984.42         37662.11
Update: Whole      1609.58    1107.31    5269.14        6575.58    4938.04      7443.11          7349.02
Update: Partial    2770.70    3416.14    6180.98        8691.78   10098.62     12026.09         11673.19
Delete             3759.62    7335.98   12801.69       13943.08    2898.83     19410.83         19232.52
Geometric Mean     5839.76    5393.59   11031.27        7291.33    4803.82     10646.07         13619.58
=============== ========== ========== ========== ============== ========== ============ ================


Results (MySQL)
===============

MariaDB 10.2 on my notebook.

=============== ========== ========== ========== ============== ========== ============ ================
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     1975.06    1508.86    1233.02        1717.99    1061.55      2459.09          7126.82
Insert: Batch      4756.06    3912.44    8683.20        6736.40    4519.06      7806.52         10516.59
Insert: Bulk      27005.60   24929.71          —       26020.77          —     49833.12         58864.29
Filter: Large     99772.15   51271.25  280891.96       80046.26   44653.69     61759.02         62879.33
Filter: Small     19763.48   17290.92  141366.74       21241.56   40362.86     21693.01         33829.54
Get                2319.24    1979.76    7593.99        2035.12    6218.80      2684.83          3526.27
Filter: dict     180824.38   64993.57  132598.83       78616.60          —     67150.55         68966.23
Filter: tuple    194938.11   65717.78  282789.77      230637.01          —     66303.28         67816.36
Update: Whole      2819.00    3223.03    5287.59        6462.97    4956.43      6344.89          4171.68
Update: Partial    3340.94    4391.66   10407.37       13115.69    8584.51      8606.25          7622.59
Delete             3290.64    4824.65   10910.95       10803.25    1780.13      8860.66          4730.91
Geometric Mean    12596.89    9745.88   24330.28       15975.86    6702.45     14791.01         16413.01
=============== ========== ========== ========== ============== ========== ============ ================

=============== ========== ========== ========== ============== ========== ============ ================
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     1214.30    1516.10    1445.84        1326.06    1219.60      1811.24          7504.58
Insert: Batch      4916.73    3887.11    7634.25        5422.79    4010.38      7925.20         10375.42
Insert: Bulk      21937.70   24543.14          —       24654.41          —     45977.92         52114.55
Filter: Large    100036.79   46069.68  251190.52       75598.13   43327.37     58006.38         60816.32
Filter: Small     19056.62   15860.06  137526.59       20271.86   38372.52     20860.29         32360.86
Get                2192.22    1838.11    7419.25        1875.26    5751.06      2513.26          3431.19
Filter: dict     174194.79   59985.09  113508.42       75280.90          —     62481.06         64254.29
Filter: tuple    190349.17   60470.52  251127.58      222938.14          —     62044.86         64765.45
Update: Whole      2606.68    3016.80    4068.78        4223.35    2569.85      2016.47          2365.43
Update: Partial    3189.96    4335.11    9028.21        8530.53   12240.67      4096.58          8666.71
Delete              648.33    4240.13    6089.52        1033.81    1391.20      4664.42          4239.59
Geometric Mean     9980.21    9181.19   21165.12       11110.55    6150.06     11049.65         15186.74
=============== ========== ========== ========== ============== ========== ============ ================

=============== ========== ========== ========== ============== ========== ============ ================
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     1077.36    1213.24    1199.76        1230.90    1104.85      1145.34          4658.74
Insert: Batch      1795.39    1927.22    2821.85        2819.24    1888.22      3476.41          5629.58
Insert: Bulk       3430.54    6288.65          —        9749.25          —     10262.50         13288.73
Filter: Large     25713.27   12007.82   55844.32       25737.91   17392.89     15715.37         14864.60
Filter: Small     10614.84    5854.79   62665.81        9490.05   16474.38      8437.61         10501.66
Get                1081.30     630.93    3945.14         818.55    3156.12      1042.08          1262.98
Filter: dict      36449.99   16396.17   20473.42       20069.71          —     16665.05         15372.02
Filter: tuple     41415.50   17372.63   54732.62       40454.07          —     16992.02         16663.86
Update: Whole      1583.10    1070.58    3039.69        4562.04    5197.24      2363.73          1891.47
Update: Partial    2976.38    3994.66    9118.01        9148.32    9556.78      4904.47          5727.31
Delete             3138.37    4214.91    6017.06        9970.96    1242.09      4779.08          6627.28
Geometric Mean      4950.0    3918.97    9865.64        7092.74    4297.75      5278.21           6720.8
=============== ========== ========== ========== ============== ========== ============ ================


Quick analysis
--------------
* Pony ORM is heavily optimised for performance.
* Django & SQLAlchemy is surprisingly similar in performance.
* Tortoise ORM is competitive.
* ``Get`` is surprisingly slow for everyone.
* Pony ORM, SQLAlchemy & SQLObject does merge operations for updates, so is technically always partial updates.
* Tortoise ORM performance using the ``asyncpg`` PostgreSQL driver is really good, winning overall.
* Tortoise ORM performance using the ``aiomysql`` MySQL driver is mediocre, the driver itself is taking the majority of CPU time.

PyPy comparison
---------------
* ``peewee`` and ``Pony ORM`` gets a noticeable performance improvement
* ``SQLAlchemy ORM`` is marginally faster
* ``Django`` is marginally slower
* ``Tortoise ORM`` is notably slower, but notably faster for Updates & Deletes
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
* ``base.executor._field_to_db()`` could be replaced with a pre-computed dict lookup
* ``Queryset.resolve_filters`` is doing lots of unnecessary stuff, especially for .get() method
* Get operation is slow (likely slow SQL generation, could be resolved with parametrized query cacheing)


On Bulk inserts
^^^^^^^^^^^^^^^
Bulk inserts is noticeably faster if inside a transaction.
We can't safely force a transaction around the entire bulk operation, so leave it as is until we have a safe chunking operation.


On Queryset performance
^^^^^^^^^^^^^^^^^^^^^^^
Since pypika is immutable, and our Queryset object is as well, we need tests to guarantee our immutability.
Then we can aggresively cache querysets.

Also, we can make more queries use parameterised queries, cache SQL generation, and cache prepared queries.

It seems in cases where we can avoid using PyPika (and use prepared statements), PyPy performance increase is even larger than CPython.


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

13) **Parametrized delete/update** *(generic)*

    | (260-280% speedup for delete operations)
    | (300-600% speedup for update operations) https://github.com/tortoise/tortoise-orm/pull/177

14) **Lazy Relation properties** *(generic)*

    (15~140% speedup for all on Test 2 (Small & Relational)) https://github.com/tortoise/tortoise-orm/pull/187

15) **Know about default converters & native DB types** *(generic)*

    (20-25% speedup for Fetch operations) https://github.com/tortoise/tortoise-orm/pull/190

16) **Connection Pooling** *(MySQL & PostgreSQL)*

    (30-50% speedup overall) https://github.com/tortoise/tortoise-orm/pull/229

17) **Many small tweaks** *(generic)*

    (5-30% depending on driver) https://github.com/tortoise/tortoise-orm/pull/241
