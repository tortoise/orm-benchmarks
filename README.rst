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

Py39:

=============== ========== ========== ========== ============== ========== ============ ==========
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max
=============== ========== ========== ========== ============== ========== ============ ==========
Insert: Single     1416.63    4800.51    1681.44         845.22    1355.40      5177.90    5177.90
Insert: Batch      4209.46    6133.01   18846.57        7329.24    4614.86      6465.41   18846.57
Insert: Bulk      14699.32   20063.64          —       16529.28          —     21500.43   21500.43
Filter: Large     79204.06   38619.57   87981.62       75709.91   30546.91     29387.52   87981.62
Filter: Small     27865.82   21981.09   11507.95       26956.97   28051.23     18312.32   28051.23
Get                3232.12    3348.96    8211.49        3377.07    6678.93      3065.70    8211.49
Filter: dict     100435.91   46279.08   90482.23       73880.67          —     36848.17  100435.91
Filter: tuple    102686.63   43784.62  115327.93      122659.60          —     32691.12  122659.60
Update: Whole      4203.50    5971.81   18950.45       16216.14   11600.25      7558.38   18950.45
Update: Partial    4844.48    6881.55   30303.48       27447.24   21985.03      8498.15   30303.48
Delete             5038.28   10847.62   42223.83       46260.71    1506.10      9109.99   46260.71
Geometric Mean    11874.16   12804.45   24120.67       19212.96    7803.47     12130.71   29348.92
=============== ========== ========== ========== ============== ========== ============ ==========

=============== ========== ========== ========== ============== ========== ============ ==========
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max
=============== ========== ========== ========== ============== ========== ============ ==========
Insert: Single     1365.84    4221.75    1537.47         764.47    1430.72      5294.97    5294.97
Insert: Batch      4115.41    5913.38   13361.91        4761.01    4751.03      5967.23   13361.91
Insert: Bulk      14112.26   19272.64          —        9509.17          —     21584.52   21584.52
Filter: Large     71100.34   32041.39  113333.53       68722.28   29544.63     29603.65  113333.53
Filter: Small     24665.50   18037.84   14405.66       24431.57   27691.02     17240.90   27691.02
Get                2957.83    2878.74    8552.12        3040.89    6625.13      3283.16    8552.12
Filter: dict      92044.94   44039.31   84377.16       63118.12          —     35849.06   92044.94
Filter: tuple     96215.08   44996.34  103819.41      104635.25          —     33943.19  104635.25
Update: Whole      4114.09    4560.58   22693.99       12916.94   12103.55      8768.18   22693.99
Update: Partial    4825.72    4144.39   32232.88       18815.85   23909.39      9958.39   32232.88
Delete              906.53   10707.40   16214.26        1175.14    1232.01      8881.57   16214.26
Geometric Mean     9623.79    11118.6   22254.87       11156.62    7759.01     12413.39   26581.81
=============== ========== ========== ========== ============== ========== ============ ==========

=============== ========== ========== ========== ============== ========== ============ ==========
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max
=============== ========== ========== ========== ============== ========== ============ ==========
Insert: Single     1148.77    2546.34    1340.20         789.53    1122.74      3537.05    3537.05
Insert: Batch      2620.62    2829.57    5058.25        5168.77    2656.47      4064.33    5168.77
Insert: Bulk       5203.72    7415.15          —       11140.84          —      7743.00   11140.84
Filter: Large     25355.59   13265.94   44475.95       31875.89   16991.79     14023.60   44475.95
Filter: Small     13861.32    7920.69    5898.15       16893.10   16025.61      9629.69   16893.10
Get                1789.53    1115.00    5396.23        2848.08    4152.90      2126.03    5396.23
Filter: dict      29545.88   18132.36   23670.09       26798.61          —     14856.68   29545.88
Filter: tuple     33378.81   19149.74   46479.18       40418.85          —     14750.00   46479.18
Update: Whole      2509.62    1465.17   17537.65       14586.52   11598.33      5633.93   17537.65
Update: Partial    4320.48    7599.34   21706.28       22256.85   20627.05      9631.31   22256.85
Delete             4962.87   10836.50   38653.62       39016.78    1406.18     10372.82   39016.78
Geometric Mean     6202.73    5825.55   13156.21       12278.92    5712.92      7453.07   15973.21
=============== ========== ========== ========== ============== ========== ============ ==========



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

PostgreSQL 14.2 on my iMac.

=============== ========== ========== ========== ============== ========== ============ ==========
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max
=============== ========== ========== ========== ============== ========== ============ ==========
Insert: Single     2256.47    2382.75    1504.28        1521.93    2387.55      5357.33    5357.33
Insert: Batch      2857.78    2973.00    6124.86        6687.88    2599.43     11721.50   11721.50
Insert: Bulk       9611.59   14513.66          —        5604.14          —     27585.03   27585.03
Filter: Large     74086.86   66188.58  141193.83       63019.80   46043.69     48271.05  141193.83
Filter: Small     22430.42   24037.38   19083.24       15553.33   33106.83     24380.37   33106.83
Get                2595.55    2618.00    7335.14        2492.64    4453.95      3171.28    7335.14
Filter: dict     102365.01   82788.31  108684.66       59944.89          —     82754.01  108684.66
Filter: tuple    106262.03   84775.09  139968.76       89798.41          —     71569.86  139968.76
Update: Whole      2954.06    3681.03    6712.28        6777.21    3747.84     13230.52   13230.52
Update: Partial    3195.64    4863.34    6717.93        8180.44    7000.83     10300.62   10300.62
Delete             3455.54    6780.28    8221.30        9841.55    2508.83     21489.49   21489.49
Geometric Mean     9952.15   11248.59   15891.13        11366.9    6388.27     18934.34   25238.04
=============== ========== ========== ========== ============== ========== ============ ==========

=============== ========== ========== ========== ============== ========== ============ ==========
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max
=============== ========== ========== ========== ============== ========== ============ ==========
Insert: Single     2280.39    2235.70     763.43         620.39    2191.50      6305.61    6305.61
Insert: Batch      3044.51    2866.67    4218.01        4045.00    2323.42     11488.73   11488.73
Insert: Bulk       9048.03   13726.61          —        5175.41          —     24209.55   24209.55
Filter: Large     72711.32   57108.09  111528.39       52640.90   40397.43     57734.35  111528.39
Filter: Small     22003.19   19362.38   11195.27       12541.27   35291.03     26081.13   35291.03
Get                2413.97    2372.59    6034.62        2095.03    4007.69      3269.57    6034.62
Filter: dict      90881.53   77617.68   83803.95       45812.02          —     79615.50   90881.53
Filter: tuple     95419.79   76708.23  128466.54       76120.75          —     73937.10  128466.54
Update: Whole      2818.49    3190.60    6161.21        4876.61    4400.54     13217.30   13217.30
Update: Partial    2637.39    4765.01    6120.75        7843.53    8726.41     16642.01   16642.01
Delete              709.12    5805.18    6430.71         723.82     982.01     18467.85   18467.85
Geometric Mean     8187.95   10176.94   12027.44        6917.04    5688.92     20014.79   24576.48
=============== ========== ========== ========== ============== ========== ============ ==========

=============== ========== ========== ========== ============== ========== ============ ==========
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max
=============== ========== ========== ========== ============== ========== ============ ==========
Insert: Single     1669.81    1022.78    1034.36        1194.71    1595.58      3933.14    3933.14
Insert: Batch      1881.93    1596.70    1971.29        3633.98    1836.82      5762.04    5762.04
Insert: Bulk       3685.42    4720.34          —        4897.94          —      8559.45    8559.45
Filter: Large     27261.29   15338.21   47862.70       28234.77   23876.31     24463.43   47862.70
Filter: Small     11990.96    7535.52    5921.78       10770.17   19802.01     14159.92   19802.01
Get                1478.74     827.99    4222.34        1833.14    2820.39      2262.50    4222.34
Filter: dict      31494.36   21782.71   24196.63       23644.00          —     28954.99   31494.36
Filter: tuple     36824.77   23457.29   48609.60       34003.18          —     28102.54   48609.60
Update: Whole      1593.23    1085.56    5911.22        5419.56    4140.70      6024.99    6024.99
Update: Partial    2679.79    4242.20    5540.77        7960.74    8316.59     17248.52   17248.52
Delete             2928.88    5554.63    9823.53        4784.40    1972.33     19447.57   19447.57
Geometric Mean     5236.56    4314.45    7880.28        6996.73    4764.27     10868.74   13350.71
=============== ========== ========== ========== ============== ========== ============ ==========


Results (MySQL)
===============

MySQL 8.0.28 on my iMac.

=============== ========== ========== ========== ============== ========== ============ ==========
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max
=============== ========== ========== ========== ============== ========== ============ ==========
Insert: Single     1750.34    2083.26    1130.52        1419.89    1802.13      6073.86    6073.86
Insert: Batch      2531.58    3323.80    3951.67        4467.49    2670.73      7316.33    7316.33
Insert: Bulk       5576.64   12127.17          —       10107.97          —     19293.91   19293.91
Filter: Large     48413.69   56925.69   79722.19       55733.07   47278.94     44182.04   79722.19
Filter: Small     11623.17   20275.97   11560.36       17919.99   33560.34     23599.43   33560.34
Get                2005.64    2598.85    5273.53        2443.46    4539.88      1696.45    5273.53
Filter: dict      56884.26   71913.45   74025.19       55739.25          —     43575.37   74025.19
Filter: tuple     59171.66   31516.29   91849.43       84673.54          —     49062.12   91849.43
Update: Whole      2483.42    2659.05    5110.92        5865.20    2193.85     10312.32   10312.32
Update: Partial    2464.70    4313.20    4468.51        9812.61    7623.10     12818.24   12818.24
Delete             2714.79    5224.38    7877.74       11384.67    1217.56     15137.37   15137.37
Geometric Mean     6850.71    9070.83   11026.13       11541.14    5383.91     14612.87    19606.4
=============== ========== ========== ========== ============== ========== ============ ==========

=============== ========== ========== ========== ============== ========== ============ ==========
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max
=============== ========== ========== ========== ============== ========== ============ ==========
Insert: Single     1278.72     847.15    1542.89        1199.07    1744.53      6541.44    6541.44
Insert: Batch      2249.83    2621.78    3679.02        3299.35    2824.39      9116.47    9116.47
Insert: Bulk       5246.88   12634.21          —        6737.19          —     19939.64   19939.64
Filter: Large     44653.67   49677.10   90349.70       52691.82   43915.73     45522.14   90349.70
Filter: Small     14861.42   18292.31   11139.12       15934.21   32443.06     25052.04   32443.06
Get                1739.97    2269.88    5387.81        2260.98    4854.13      3470.66    5387.81
Filter: dict      52201.94   65597.84   70097.25       50468.72          —     54344.91   70097.25
Filter: tuple     51012.56   66040.24   87542.74       72008.10          —     51308.56   87542.74
Update: Whole      1884.75    2755.86    4981.60        4959.51    3617.87     11440.66   11440.66
Update: Partial    2482.05    4277.53    6235.59        8074.72    7548.60     14003.55   14003.55
Delete              622.80    5434.00    3784.50         801.68    1313.84      9874.00    9874.00
Geometric Mean     5485.14    8468.37   10830.37        7731.81    5766.53     16242.65   19789.49
=============== ========== ========== ========== ============== ========== ============ ==========

=============== ========== ========== ========== ============== ========== ============ ==========
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max
=============== ========== ========== ========== ============== ========== ============ ==========
Insert: Single     1228.59    1364.09    1169.95        1166.69     300.30       368.73    1364.09
Insert: Batch      1579.98    1848.77    2077.19        2410.57     820.81      1658.10    2410.57
Insert: Bulk       2971.42    5117.75          —        5539.81          —      1361.95    5539.81
Filter: Large     23917.93   15991.72   41673.83       26783.78   24057.01     17401.20   41673.83
Filter: Small     10086.80    7445.39    4142.09       11849.35   19443.10     10717.24   19443.10
Get                1316.96     917.24    3549.25        1946.06    2954.43      1629.59    3549.25
Filter: dict      26542.31   22718.17   22319.98       22800.17          —     20092.73   26542.31
Filter: tuple     29222.15   24281.26   42298.35       32783.62          —     17916.90   42298.35
Update: Whole      1567.04    1077.08    4272.23        4429.93    1276.06      3669.59    4429.93
Update: Partial    2644.92    4137.01    5993.23        7719.81    4822.29      7138.44    7719.81
Delete             2741.45    5506.19    7441.53        6708.85     217.53      7121.31    7441.53
Geometric Mean     4521.58    4590.54    6962.83        6885.86    2149.64      4542.56    8414.22
=============== ========== ========== ========== ============== ========== ============ ==========



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
