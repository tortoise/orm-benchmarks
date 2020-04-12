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
Insert: Single     3708.87    5988.94    5313.19        1787.23    3588.88      8771.86
Insert: Batch      5202.03    7080.62   20682.10        9936.82    5334.61     11856.23
Insert: Bulk      22641.95   34830.97          —       36263.39          —     92215.74
Filter: Large     70827.06   40292.41  186303.67       80556.02   25142.92    192864.71
Filter: Small     16590.77   16877.80   11548.63       16673.05   30017.21     24988.74
Get                2779.47    3388.39    9462.00        2539.36    6495.46      4594.26
Filter: dict      95383.31   59175.90  106239.43       84593.08          —    350127.46
Filter: tuple    108427.53   59130.16  182755.44      315451.73          —    274481.55
Update: Whole      3393.08    5845.30   22510.83       18488.72   12466.46     12511.45
Update: Partial    3858.61    7641.23   33949.08       27403.46   25063.86     15675.48
Delete             4053.31   11102.10   49233.60       51217.01    4524.37     21317.97
Geometric Mean    12057.43   14488.47   33214.84       23999.02   10359.79     34608.93
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     3792.99    5908.45    4372.95        1524.62    3523.61      7895.02
Insert: Batch      5654.38    7053.93   12926.10        7658.25    5111.69     10408.76
Insert: Bulk      29279.34   39363.14          —       35258.07          —     75826.76
Filter: Large     64538.00   37145.51  171533.69       75314.01   23816.30    184173.90
Filter: Small     15956.43   15534.93   11179.07       15441.66   28059.24     21580.55
Get                2562.68    3223.44    9296.92        2320.04    6217.74      4337.92
Filter: dict      99764.89   56453.19   93591.43       80442.21          —    312701.05
Filter: tuple    106787.45   56067.35  172917.39      275313.93          —    250906.92
Update: Whole      3348.87    5222.23   21098.72       10609.32   12188.22     11640.96
Update: Partial    3729.84    7827.97   28350.00       12911.73   25747.75     16260.29
Delete              696.88   11288.93   22724.49         454.02    3001.32       716.91
Geometric Mean    10398.37   14122.67   27200.16       12814.38    9572.29     23385.29
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     2285.04    2751.28    2737.64        1349.44    1874.19      5093.77
Insert: Batch      2750.78    3021.59    3091.32        4383.33    2229.89      7070.07
Insert: Bulk       5291.40    8754.71          —       16402.96          —     19653.12
Filter: Large     22412.18   13183.41   47158.46       24323.79   11602.84     19114.16
Filter: Small      9390.76    6659.39    4502.35        7188.04   12570.42     10912.18
Get                1612.12    1106.54    5267.01         919.54    3327.73      2306.87
Filter: dict      28593.42   19793.13   18716.68       19076.15          —     24312.88
Filter: tuple     31420.22   20820.41   47397.64       40602.88          —     24049.88
Update: Whole      2230.23    1415.37   15934.15       12590.54   10872.54      7509.95
Update: Partial    3539.24    7516.68   20600.17       14820.40   22048.41     17292.82
Delete             3966.97   11245.15   35715.83       28116.76    2919.47     12186.04
Geometric Mean     5927.64    5978.24   12569.35        9594.03    5875.18     11099.88
=============== ========== ========== ========== ============== ========== ============


PyPy7.3-Py3.6: (Outdated)

=============== ========== ========== ========== ============== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     4092.94    6042.45    6166.89        1004.98      6786.58
Insert: Batch      4529.93    6456.81   18247.22        6982.63     26348.64
Insert: Bulk      17961.11   24302.27          —       21428.22     80531.38
Filter: Large    152801.52   91886.54  295678.67      129700.40     90993.88
Filter: Small      6099.36   65094.77  175134.68       60966.19     45463.05
Get                4255.07    6793.41    8310.16        4339.15      9229.52
Filter: dict     147533.08  116293.38  215108.01      109211.59     94985.63
Filter: tuple    175529.83  122951.45  281181.48      253415.27    130914.54
Update: Whole      6710.01   16514.91   41939.12       22677.70     30434.61
Update: Partial    8089.69   23377.04   51308.13       43023.59     38576.48
Delete             8766.41   29169.88   74799.44       81948.65     42805.28
Geometric Mean    15887.12   27270.66   58524.96       28825.51     39281.41
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     4089.62    5982.16    5927.49         818.31      8128.96
Insert: Batch      4582.76    6909.47   15558.25        6012.19     25381.23
Insert: Bulk      16201.10   24021.67          —       20294.09     77993.66
Filter: Large    138968.39   90818.94  279382.51      118860.29     71640.16
Filter: Small      5439.62   62951.57  168192.03       52251.13     38208.34
Get                4092.11    6989.34    8230.02        3379.57      8430.82
Filter: dict     134900.00  112626.68  202932.98       94477.51     71689.52
Filter: tuple    159685.66  122797.29  274293.13      223882.76    119104.10
Update: Whole      6201.26   11396.24   35644.86       17562.70     28303.72
Update: Partial    7669.88   23086.17   41247.77       25492.40     35430.58
Delete             2087.76   34330.64   38098.81         633.66       369.97
Geometric Mean    13135.78   26719.72   50653.72       15519.07     23445.05
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     2194.07    3827.50    4030.12         792.54      5429.88
Insert: Batch      2072.86    3928.59    7509.87        4841.25     15489.04
Insert: Bulk       4747.82    9996.01          —       15407.30     29085.53
Filter: Large     25016.73   30627.76  122459.86       37727.96      2968.21
Filter: Small      1508.74   24123.13   98162.15       21523.32      2454.28
Get                2231.56    4443.86    6313.33        2312.70      1490.23
Filter: dict      29467.52   40064.73   81433.44       27085.70      3001.12
Filter: tuple     31329.65   46774.06  123617.06       45894.78      8845.51
Update: Whole      4220.60    6984.34   29109.60       10686.28     11302.96
Update: Partial    7346.76   21125.93   33835.74       14716.48     24182.52
Delete             9083.28   31221.47   64601.85       64029.41     41709.27
Geometric Mean     6146.34   14064.74   32867.64       12702.84      7951.76
=============== ========== ========== ========== ============== ============


Results (PostgreSQL)
====================

PostgreSQL 11.4 on my notebook.

=============== ========== ========== ========== ============== ========== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     3046.49    3035.44    3361.12        1814.48    3238.90      7541.86
Insert: Batch      3419.05    3039.08    6920.32        4566.33    3037.27     18944.74
Insert: Bulk      19943.97   24825.96          —       10144.37          —     50390.38
Filter: Large    160573.42  101541.38  293009.63       88200.07   45704.61    260929.54
Filter: Small      7444.57    8485.52    6340.09        6484.99   28120.82     15273.01
Get                2073.64    2676.61    7045.77        1906.96    5583.03      2944.01
Filter: dict     457340.75  203236.43  133438.41       85812.46          —    501655.20
Filter: tuple    604813.35  209329.41  289008.12      365515.41          —    409232.20
Update: Whole      2061.79    3441.69    6281.25        6780.58    4381.82     20045.23
Update: Partial    2305.92    4246.32    8372.84        9854.83    8749.16     20041.56
Delete             2743.33    6697.27   11440.59       12389.69    4210.74     25087.36
Geometric Mean    13042.56   13244.22   19271.14       13339.95    7622.37     36940.07
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     3000.14    3066.30    3041.99        1584.19    3301.96      8225.73
Insert: Batch      3275.10    3207.58    6071.49        4357.21    3439.71     18554.31
Insert: Bulk      16513.85   24897.11          —       10157.87          —     49081.10
Filter: Large    136591.30   85849.56  269724.96       84504.61   45003.67    244791.73
Filter: Small      7941.31   10370.58    6658.11        7704.75   31769.32     26261.45
Get                1916.72    2602.08    7204.73        1810.57    5501.74      3071.52
Filter: dict     426788.08  179673.18  116074.73       82222.43          —    525064.22
Filter: tuple    602467.44  185449.39  262208.81      357270.05          —    405270.91
Update: Whole      2056.47    3244.28    6594.24        5454.02    4407.83     20271.90
Update: Partial    1997.14    4231.52    8329.78        7270.69    9336.57     23277.88
Delete              495.98    6073.53    6763.22         237.68     711.17      1607.63
Geometric Mean    10531.14   12849.01   17505.24        8745.34    6341.32     30825.32
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     1704.46    1286.58    1335.46         692.97     851.48      2573.48
Insert: Batch      1733.87    1295.53    1416.18        1152.96     868.25      4935.20
Insert: Bulk       3212.54    4749.81          —        2718.80          —      8988.51
Filter: Large     33070.46   15044.68   37238.26       19434.78    9239.06     21633.83
Filter: Small      4638.39    3410.35    1749.43        2302.21    8364.07      4533.75
Get                1141.54     709.98    2583.91         408.66    1524.24      1040.07
Filter: dict      42689.93   28491.20   13034.79       16012.10          —     33628.66
Filter: tuple     50033.52   30122.55   33604.91       29556.18          —     29609.60
Update: Whole      1241.53     773.16    3234.47        2882.86    2030.25      5421.10
Update: Partial    1702.65    2886.94    2893.40        4088.44    4261.02      9066.73
Delete             2131.09    4930.29    5057.99        6613.28    1269.93     12135.44
Geometric Mean     4517.63    3846.06    4807.96        3635.26    2358.28      7843.98
=============== ========== ========== ========== ============== ========== ============


Results (MySQL)
===============

MariaDB 10.2 on my notebook.

=============== ========== ========== ========== ============== ========== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     1383.62    1266.45    1434.83         901.20    1197.20      3080.33
Insert: Batch      2043.80    2001.30    4995.87        3203.36    2096.42      5002.17
Insert: Bulk      15038.21   14595.01          —       14492.72          —     25766.89
Filter: Large     54917.59   26408.01  159944.32       47911.41   23953.85     31345.78
Filter: Small      2036.85    1865.41    1956.58        1929.00   21794.98      3345.87
Get                1181.04    1003.87    4031.27        1103.81    2866.85      1654.70
Filter: dict      88357.33   32639.37   74397.80       44173.61          —     35968.88
Filter: tuple     96285.53   32741.59  160698.59      103112.61          —     33153.43
Update: Whole      1263.76    1586.54    3442.20        3895.25    2678.92      4518.65
Update: Partial    1464.38    2032.87    5431.92        6084.50    5363.30      6197.01
Delete             1509.27    2516.67    4844.72        5806.70     780.58      6296.95
Geometric Mean     5478.73    4514.32    9979.18         7195.1    3785.07      8389.33
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     1140.07    1205.60    1319.47         692.64    1697.55      7266.86
Insert: Batch      1913.20    1946.12    3799.29        2430.65    3030.68     10719.92
Insert: Bulk      11963.18   13910.01          —       12706.30          —     47720.62
Filter: Large     49080.26   23384.97  147540.42       39652.98   38730.28     57755.11
Filter: Small      1987.13    1780.89    1810.24        1691.17   35158.66     11597.94
Get                1091.36     944.56    3980.25        1036.55    4473.41      3250.60
Filter: dict      87343.79   30594.16   65027.52       68619.67          —     66965.77
Filter: tuple     93483.79   30982.03  145219.36      168441.70          —     62954.08
Update: Whole      1207.88    1472.01    2557.32        5012.41    4588.85     10466.75
Update: Partial    1423.73    2082.51    4228.22        7047.10    9078.71     13840.88
Delete              297.26    2362.13    2883.80         860.74     758.49     12907.51
Geometric Mean     4387.32    4279.26    8309.39        6202.36    5616.56     17988.23
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     1314.33    1307.00    1268.69        1022.36    1100.24      4518.38
Insert: Batch      1701.32    1827.67    2406.95        2336.97    1631.93      5843.68
Insert: Bulk       3236.68    5640.79          —        8049.09          —     13054.61
Filter: Large     25250.38   11090.04   52755.70       21242.17   15361.81     14555.25
Filter: Small       529.70     522.92     706.59         518.68   14567.92      2532.96
Get                1191.19     580.02    3617.59         756.61    2503.35      1196.82
Filter: dict      32249.89   15036.99   20121.97       17358.19          —     17668.97
Filter: tuple     35866.84   15692.52   53808.64       30795.17          —     16545.91
Update: Whole      1323.77     978.24    4530.36        5151.14    3685.97      5964.25
Update: Partial    2133.01    3362.62    6607.78        7412.20    9167.75     13035.97
Delete             2228.91    3958.71    6360.09        7737.63    1053.44     13189.97
Geometric Mean     3455.77     2935.1    6207.05        4710.19    3708.91      7552.43
=============== ========== ========== ========== ============== ========== ============


PyPy7.3-Py3.6: (Outdated)

=============== ========== ========== ========== ============== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     2479.55    2663.10    3088.68         686.92      3311.91
Insert: Batch      3478.12    4571.76    5194.87        4214.03     13584.52
Insert: Bulk      14553.90   19480.48          —       15260.41     55214.98
Filter: Large     80983.35  175029.85  479457.80       59215.04    160185.46
Filter: Small      4995.72   37628.16  136060.23       18990.66     24888.53
Get                2868.25    4870.54    6107.97        2630.39      6538.67
Filter: dict      80650.88  219339.95  301358.89       52242.19    183104.50
Filter: tuple     93584.59  257332.26  490594.29       74740.17    175407.06
Update: Whole      3563.43    7760.36    5348.80        5540.23     11161.77
Update: Partial    4536.02   10036.94   11210.07       12264.97     14984.03
Delete             4978.72   10073.98   11107.52       10907.25     12449.24
Geometric Mean     9889.22   20926.09   30192.66       11285.31     26393.92
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     2266.32    2663.82    2669.34         597.25      3513.88
Insert: Batch      3328.18    4435.96    6949.97        3773.89     10493.08
Insert: Bulk      14065.42   18684.71          —       14458.93     55861.34
Filter: Large     80296.63  164763.64  447302.97       54498.39    153077.80
Filter: Small      4800.15   35434.65  130211.62       17627.65     21258.96
Get                2565.44    4543.19    5849.48        2310.20      6251.27
Filter: dict      77842.51  207108.12  280970.71       50958.86    185933.49
Filter: tuple     91267.58  239574.53  438762.04       73630.97    172285.95
Update: Whole      2701.75    5406.82    6975.43        4327.97      9913.26
Update: Partial    4539.54    9879.36   10746.90       10125.79     14495.50
Delete             1176.44    7017.19    6249.98        1387.88      8181.26
Geometric Mean     8165.06   18884.27   28591.56        8489.41     24079.39
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     1008.08    1582.11    1617.94         465.03      2258.82
Insert: Batch      1492.21    2833.39    3595.88        2126.38      6739.82
Insert: Bulk       3357.71    6484.93          —        6410.32     16790.12
Filter: Large     12164.83   40576.68  109275.41        9531.62     34746.82
Filter: Small      2314.81   12551.29   58031.65        5503.53      9873.51
Get                1083.01    2165.71    2800.69         854.14      2358.51
Filter: dict      12742.82   54209.15   73098.84        8640.37     46526.40
Filter: tuple     13728.33   62009.01  107794.63       10255.39     42013.15
Update: Whole      1589.21    2352.14    4388.50        3946.67      5021.95
Update: Partial    3894.78    8822.50    6142.39        7243.80     14487.33
Delete             3791.23    8238.25    8413.57        8394.18     11540.60
Geometric Mean      3367.9    8574.74   13385.55         4134.8     11175.14
=============== ========== ========== ========== ============== ============


Quick analysis
--------------
* Pony ORM is heavily optimised for performance.
* Django & SQLAlchemy is surprisingly similar in performance.
* Tortoise ORM is competitive.
* ``Get`` is surprisingly slow for everyone.
* Pony ORM, SQLAlchemy & SQLObject does merge operations for updates, so is technically always partial updates.
* Tortoise ORM performance using the ``asyncpg`` PostgreSQL driver is really good, winning overall.
* Tortoise ORM performance using the ``aiomysql`` MySQL driver is mediocre, the driver itself is taking the majority of CPU time. PyPy runs this driver a lot faster, which indicates that the slow paths are likely just in Python itself.

PyPy comparison: SQLite
-----------------------
* ``peewee`` and ``Pony ORM`` gets a noticeable performance improvement
* ``SQLAlchemy ORM`` and ``Django`` performs similarily
* ``Tortoise ORM`` has slow Reads and fast Create, Update & Delete operation
* ``SQLObject`` fails

PyPy comparison: MySQL
-----------------------
* ``peewee`` and ``Tortoise ORM`` gets a noticeable performance improvement
* ``Pony ORM`` is marginally faster
* ``SQLAlchemy ORM`` and ``Django`` is marginally slower
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


On Queryset performance
^^^^^^^^^^^^^^^^^^^^^^^
Since pypika is immutable, and our Queryset object is as well, we need tests to guarantee our immutability.
Then we can aggresively cache querysets.

Also, we can make more queries use parameterised queries, cache SQL generation, and cache prepared queries.

It seems in cases where we can cache the PyPika result (and use prepared statements), PyPy performance increase is even larger than CPython.


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
