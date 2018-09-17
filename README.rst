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
SQLAlchemy ORM:
        http://www.sqlalchemy.org/
SQLObject:
        https://github.com/sqlobject/sqlobject
Tortoise ORM:
        https://github.com/tortoise/tortoise-orm

Results
=======

==================== ============ ============ ============
\                     Django       peewee       Pony
==================== ============ ============ ============
Insert                   1163.99      1225.21      1454.15
Insert: atomic           8476.31      6975.57     24868.60
Insert: bulk            34120.59     11528.16            —
Filter: match           68934.47     39307.05    223419.30
Filter: contains        68340.79     39641.32    226013.34
==================== ============ ============ ============
