# ORM Benchmarks

Comprehensive performance benchmarks comparing popular Python ORMs across PostgreSQL, MySQL, and SQLite.

**Tested ORMs:**

| ORM | Type | PostgreSQL | MySQL | SQLite |
|-----|------|:---:|:---:|:---:|
| [Tortoise ORM](https://github.com/tortoise/tortoise-orm) | async | asyncpg | asyncmy | aiosqlite |
| [Django](https://www.djangoproject.com/) | sync | psycopg2 | mysqlclient | sqlite3 |
| [peewee](https://github.com/coleifer/peewee) | sync | psycopg2 | pymysql | sqlite3 |
| [SQLAlchemy ORM (async)](http://www.sqlalchemy.org/) | async | asyncpg | aiomysql | aiosqlite |
| [SQLObject](https://github.com/sqlobject/sqlobject) | sync | psycopg2 | mysqlclient | sqlite3 |
| [Piccolo](https://github.com/piccolo-orm/piccolo) | async | asyncpg | — | aiosqlite |
| [ormar](https://github.com/collerek/ormar) | async | asyncpg | aiomysql | aiosqlite |
| [SQLModel](https://github.com/tiangolo/sqlmodel) | async | asyncpg | aiomysql | aiosqlite |

> **Environment:** Python 3.14, macOS (Apple Silicon), 100 iterations per operation.
> Piccolo does not support MySQL.

## Operations

| Code | Operation | Description |
|------|-----------|-------------|
| A | Insert: Single | Insert one row at a time |
| B | Insert: Batch | Insert many rows in a single transaction |
| C | Insert: Bulk | Use bulk insert operations |
| D | Filter: Large | Fetch a large result set |
| E | Filter: Small | Fetch limit 20 with random offset |
| F | Get | Fetch a single row by primary key |
| G | Filter: dict | Fetch large result set as dicts |
| H | Filter: tuple | Fetch large result set as tuples |
| I | Update: Whole | Update all fields of a row |
| J | Update: Partial | Update a single field |
| K | Delete | Delete a single row |

## Test Models

**Test 1 — Simple model** (4 fields): `id`, `timestamp`, `level` (indexed), `text` (indexed)

**Test 2 — FK relations**: Same as Test 1, plus self-referential foreign key, reverse FK, and M2M relation

**Test 3 — Wide model** (32+ fields): Same as Test 1, plus 4 sets of 8 typed columns (float, smallint, int, bigint, char, text, decimal, json) — 2 with defaults, 2 nullable

---

## Results: PostgreSQL 17

PostgreSQL 17 in Docker. Driver: `asyncpg` for async ORMs, `psycopg2` for sync ORMs.

### Overview

![PostgreSQL Summary](images/pg_summary.png)

### Test 1: Simple Model (4 fields)

![PostgreSQL Test 1](images/pg_test1.png)

| Operation | Django | peewee | SA ORM async | SQLObject | Tortoise ORM | Piccolo | ormar | SQLModel | Best |
|-----------|--------|--------|--------------|-----------|--------------|---------|-------|----------|------|
| Insert: Single | 776 | 651 | 584 | 699 | **3,455** | 3,240 | 283 | 540 | Tortoise ORM |
| Insert: Batch | 2,069 | 2,418 | 1,154 | 1,575 | **14,033** | 12,138 | 1,048 | 1,081 | Tortoise ORM |
| Insert: Bulk | 5,224 | 5,009 | 1,264 | — | **18,807** | 18,060 | 1,178 | 1,079 | Tortoise ORM |
| Filter: Large | 57,451 | 62,009 | 32,318 | 50,694 | 143,810 | **147,031** | 19,735 | 32,389 | Piccolo |
| Filter: Small | 19,491 | 18,066 | 7,532 | 24,844 | **60,699** | 45,805 | 5,501 | 6,444 | Tortoise ORM |
| Get | 2,183 | 2,590 | 1,894 | 3,341 | 6,420 | **6,854** | 846 | 1,792 | Piccolo |
| Filter: dict | 64,394 | 81,652 | 33,798 | — | 209,380 | **328,124** | 26,777 | 31,117 | Piccolo |
| Filter: tuple | 55,080 | 66,827 | 37,933 | — | 197,175 | **332,310** | 23,286 | 34,411 | Piccolo |
| Update: Whole | 2,896 | 3,555 | 1,743 | 1,995 | **17,407** | 13,491 | 2,538 | 1,781 | Tortoise ORM |
| Update: Partial | 3,281 | 4,812 | 1,526 | 3,802 | **18,255** | 16,180 | 2,740 | 1,856 | Tortoise ORM |
| Delete | 3,386 | 5,701 | 1,869 | 843 | **21,010** | 18,968 | 2,890 | 1,895 | Tortoise ORM |
| **Geometric Mean** | 7,108 | 8,257 | 3,816 | 3,622 | 29,381 | **29,514** | 3,233 | 3,660 | **Piccolo** |

### Test 2: FK Relations

![PostgreSQL Test 2](images/pg_test2.png)

| Operation | Django | peewee | SA ORM async | SQLObject | Tortoise ORM | Piccolo | ormar | SQLModel | Best |
|-----------|--------|--------|--------------|-----------|--------------|---------|-------|----------|------|
| Insert: Single | 765 | 822 | 564 | 517 | **3,350** | 3,075 | 264 | 521 | Tortoise ORM |
| Insert: Batch | 2,654 | 2,477 | 1,184 | 1,140 | **12,355** | 8,785 | 1,067 | 1,061 | Tortoise ORM |
| Insert: Bulk | 4,733 | 5,863 | 1,146 | — | **21,969** | 12,461 | 1,157 | 1,120 | Tortoise ORM |
| Filter: Large | 59,181 | 58,026 | 32,641 | 47,745 | **137,275** | 115,754 | 14,400 | 32,614 | Tortoise ORM |
| Filter: Small | 16,460 | 19,514 | 6,792 | 29,200 | 47,951 | **50,408** | 4,899 | 8,051 | Piccolo |
| Get | 2,394 | 2,605 | 1,905 | 1,440 | **5,870** | 5,665 | 787 | 1,922 | Tortoise ORM |
| Filter: dict | 73,174 | 78,313 | 33,632 | — | 207,239 | **303,737** | 25,848 | 31,831 | Piccolo |
| Filter: tuple | 65,459 | 70,256 | 34,130 | — | 192,246 | **284,733** | 29,597 | 36,273 | Piccolo |
| Update: Whole | 3,216 | 3,791 | 1,598 | 1,907 | **16,647** | 12,217 | 2,400 | 1,665 | Tortoise ORM |
| Update: Partial | 3,392 | 4,586 | 1,729 | 4,022 | **18,796** | 15,065 | 2,442 | 1,781 | Tortoise ORM |
| Delete | 866 | 5,880 | 896 | 629 | **17,921** | 12,984 | 2,940 | 1,711 | Tortoise ORM |
| **Geometric Mean** | 6,587 | 8,631 | 3,484 | 2,949 | **27,860** | 24,918 | 3,082 | 3,710 | **Tortoise ORM** |

### Test 3: Wide Model (32+ fields)

![PostgreSQL Test 3](images/pg_test3.png)

| Operation | Django | peewee | SA ORM async | SQLObject | Tortoise ORM | Piccolo | ormar | SQLModel | Best |
|-----------|--------|--------|--------------|-----------|--------------|---------|-------|----------|------|
| Insert: Single | 660 | 712 | 555 | 683 | 1,560 | **2,761** | 177 | 507 | Piccolo |
| Insert: Batch | 1,580 | 1,338 | 1,137 | 1,280 | **8,077** | 4,627 | 542 | 953 | Tortoise ORM |
| Insert: Bulk | 3,374 | 3,074 | 1,187 | — | **9,571** | 5,596 | 814 | 971 | Tortoise ORM |
| Filter: Large | 32,188 | 25,686 | 26,031 | 26,710 | **50,995** | 29,431 | 2,893 | 23,445 | Tortoise ORM |
| Filter: Small | 8,946 | 9,546 | 7,167 | 20,497 | **31,247** | 18,652 | 2,105 | 5,997 | Tortoise ORM |
| Get | 1,541 | 1,311 | 1,773 | 2,288 | **5,056** | 3,563 | 626 | 1,708 | Tortoise ORM |
| Filter: dict | 28,900 | 32,299 | 22,351 | — | 71,887 | **121,813** | 6,883 | 22,634 | Piccolo |
| Filter: tuple | 34,619 | 30,980 | 29,794 | — | 66,990 | **121,798** | 6,353 | 29,111 | Piccolo |
| Update: Whole | 2,067 | 1,386 | 1,620 | 2,150 | **12,590** | 5,181 | 1,375 | 1,559 | Tortoise ORM |
| Update: Partial | 3,113 | 3,960 | 1,689 | 3,873 | **19,986** | 5,512 | 59 | 1,680 | Tortoise ORM |
| Delete | 3,480 | 4,915 | 1,728 | 769 | **22,214** | 14,305 | 2,595 | 1,574 | Tortoise ORM |
| **Geometric Mean** | 4,851 | 4,712 | 3,432 | 3,025 | **16,587** | 12,145 | 1,097 | 3,152 | **Tortoise ORM** |

---

## Results: MySQL 8

MySQL 8 in Docker. Driver: `asyncmy` for Tortoise, `aiomysql` for SA async / ormar, `mysqlclient` for Django, `pymysql` for peewee / SQLObject. Piccolo does not support MySQL.

### Overview

![MySQL Summary](images/mysql_summary.png)

### Test 1: Simple Model (4 fields)

![MySQL Test 1](images/mysql_test1.png)

| Operation | Django | peewee | SA ORM async | SQLObject | Tortoise ORM | ormar | SQLModel | Best |
|-----------|--------|--------|--------------|-----------|--------------|-------|----------|------|
| Insert: Single | 460 | 475 | 1,260 | 386 | **2,226** | 1,218 | 1,198 | Tortoise ORM |
| Insert: Batch | 1,685 | 3,403 | 4,425 | 1,743 | **10,352** | 3,903 | 3,639 | Tortoise ORM |
| Insert: Bulk | 2,888 | 8,244 | 4,704 | — | **13,545** | 5,669 | 3,614 | Tortoise ORM |
| Filter: Large | 53,093 | 57,706 | 70,552 | 49,274 | **98,361** | 29,059 | 62,415 | Tortoise ORM |
| Filter: Small | 13,216 | 19,768 | 31,251 | 23,637 | **52,596** | 16,702 | 33,064 | Tortoise ORM |
| Get | 2,058 | 2,065 | 4,486 | 3,340 | **6,891** | 1,753 | 4,132 | Tortoise ORM |
| Filter: dict | 65,185 | 64,735 | 77,599 | — | **126,411** | 67,878 | 65,702 | Tortoise ORM |
| Filter: tuple | 62,068 | 57,817 | 101,337 | — | **124,069** | 69,064 | 99,444 | Tortoise ORM |
| Update: Whole | 2,422 | 3,203 | 2,376 | 2,211 | **12,485** | 5,086 | 2,152 | Tortoise ORM |
| Update: Partial | 3,568 | 4,624 | 2,510 | 6,088 | **14,040** | 6,045 | 2,439 | Tortoise ORM |
| Delete | 3,421 | 4,937 | 2,574 | 406 | **13,740** | 8,243 | 2,515 | Tortoise ORM |
| **Geometric Mean** | 6,035 | 8,000 | 8,998 | 3,307 | **21,351** | 8,885 | 8,221 | **Tortoise ORM** |

### Test 2: FK Relations

![MySQL Test 2](images/mysql_test2.png)

| Operation | Django | peewee | SA ORM async | SQLObject | Tortoise ORM | ormar | SQLModel | Best |
|-----------|--------|--------|--------------|-----------|--------------|-------|----------|------|
| Insert: Single | 477 | 525 | 1,173 | 399 | **1,777** | 952 | 1,063 | Tortoise ORM |
| Insert: Batch | 2,458 | 3,374 | 4,873 | 1,825 | **8,299** | 3,278 | 3,853 | Tortoise ORM |
| Insert: Bulk | 4,029 | **12,401** | 3,807 | — | 7,852 | 5,261 | 3,452 | peewee |
| Filter: Large | 60,201 | 50,582 | 71,476 | 46,076 | **95,298** | 21,057 | 69,532 | Tortoise ORM |
| Filter: Small | 13,404 | 14,109 | 26,652 | 21,838 | **58,097** | 8,354 | 31,293 | Tortoise ORM |
| Get | 2,146 | 2,171 | 3,965 | 3,227 | **7,188** | 1,719 | 4,333 | Tortoise ORM |
| Filter: dict | 70,525 | 63,725 | 70,878 | — | **122,091** | 48,115 | 54,117 | Tortoise ORM |
| Filter: tuple | 59,955 | 42,729 | 102,362 | — | **120,419** | 41,905 | 103,458 | Tortoise ORM |
| Update: Whole | 2,443 | 3,229 | 2,026 | 2,140 | **7,588** | 4,045 | 2,187 | Tortoise ORM |
| Update: Partial | 3,774 | 3,953 | 2,183 | 4,642 | **11,806** | 5,555 | 2,565 | Tortoise ORM |
| Delete | 917 | 5,191 | 883 | 328 | **12,982** | 5,491 | 2,461 | Tortoise ORM |
| **Geometric Mean** | 5,883 | 7,759 | 7,567 | 3,061 | **18,337** | 6,707 | 8,134 | **Tortoise ORM** |

### Test 3: Wide Model (32+ fields)

![MySQL Test 3](images/mysql_test3.png)

| Operation | Django | peewee | SA ORM async | SQLObject | Tortoise ORM | ormar | SQLModel | Best |
|-----------|--------|--------|--------------|-----------|--------------|-------|----------|------|
| Insert: Single | 368 | 366 | 1,318 | 342 | **1,331** | 703 | 1,071 | Tortoise ORM |
| Insert: Batch | 1,583 | 2,076 | 4,225 | 1,372 | **4,384** | 860 | 2,405 | Tortoise ORM |
| Insert: Bulk | 2,623 | 3,506 | 3,403 | — | **6,167** | 2,290 | 2,400 | Tortoise ORM |
| Filter: Large | 30,557 | 16,564 | 27,000 | 30,339 | **35,672** | 3,393 | 22,934 | Tortoise ORM |
| Filter: Small | 8,812 | 6,830 | 14,421 | 16,180 | **23,723** | 2,765 | 14,136 | Tortoise ORM |
| Get | 1,616 | 1,017 | 2,270 | 2,656 | **4,014** | 839 | 2,187 | Tortoise ORM |
| Filter: dict | 30,032 | 18,525 | 22,793 | — | **48,723** | 7,504 | 22,733 | Tortoise ORM |
| Filter: tuple | 35,392 | 21,983 | 31,740 | — | **41,779** | 7,659 | 29,487 | Tortoise ORM |
| Update: Whole | 1,852 | 1,590 | 1,456 | 2,207 | **8,684** | 1,715 | 1,410 | Tortoise ORM |
| Update: Partial | 3,407 | 4,148 | 1,512 | 5,091 | **13,981** | 5,052 | 1,517 | Tortoise ORM |
| Delete | 3,166 | 4,352 | 1,559 | 401 | **16,320** | 7,646 | 1,450 | Tortoise ORM |
| **Geometric Mean** | 4,466 | 3,943 | 4,928 | 2,692 | **11,560** | 2,629 | 4,292 | **Tortoise ORM** |

---

## Results: SQLite

SQLite on local filesystem (`/tmp/db.sqlite3`). This benchmark is inherently single-threaded due to SQLite's write lock — async ORMs pay overhead without concurrency benefit.

### Overview

![SQLite Summary](images/sqlite_summary.png)

### Test 1: Simple Model (4 fields)

![SQLite Test 1](images/sqlite_test1.png)

| Operation | Django | peewee | SA ORM async | SQLObject | Tortoise ORM | Piccolo | ormar | SQLModel | Best |
|-----------|--------|--------|--------------|-----------|--------------|---------|-------|----------|------|
| Insert: Single | 2,177 | **6,887** | 1,247 | 2,368 | 5,693 | 922 | 982 | 755 | peewee |
| Insert: Batch | 13,050 | **15,823** | 788 | 12,294 | 12,693 | 473 | 787 | 742 | peewee |
| Insert: Bulk | 19,043 | **37,108** | 783 | — | 33,060 | 772 | 1,957 | 727 | peewee |
| Filter: Large | **181,041** | 87,912 | 39,863 | 84,364 | 167,777 | 39,248 | 26,140 | 40,523 | Django |
| Filter: Small | 55,653 | 47,699 | 26,652 | **79,460** | 78,915 | 21,409 | 13,599 | 24,095 | SQLObject |
| Get | 8,475 | 8,587 | 3,567 | **19,691** | 9,168 | 2,697 | 2,308 | 3,506 | SQLObject |
| Filter: dict | 223,613 | 118,764 | 50,330 | — | **272,534** | 51,683 | 56,673 | 50,218 | Tortoise ORM |
| Filter: tuple | 231,802 | 121,041 | 59,008 | — | **253,995** | 51,491 | 50,314 | 63,741 | Tortoise ORM |
| Update: Whole | 11,260 | 15,287 | 780 | **28,612** | 20,541 | 1,409 | 1,096 | 781 | SQLObject |
| Update: Partial | 13,214 | 21,100 | 792 | **51,521** | 25,921 | 1,132 | 1,117 | 797 | SQLObject |
| Delete | 14,542 | **28,985** | 780 | 2,595 | 27,807 | 1,432 | 1,117 | 788 | peewee |
| **Geometric Mean** | 26,828 | 30,273 | 3,998 | 18,661 | **38,766** | 4,037 | 4,052 | 3,770 | **Tortoise ORM** |

### Test 2: FK Relations

![SQLite Test 2](images/sqlite_test2.png)

| Operation | Django | peewee | SA ORM async | SQLObject | Tortoise ORM | Piccolo | ormar | SQLModel | Best |
|-----------|--------|--------|--------------|-----------|--------------|---------|-------|----------|------|
| Insert: Single | 2,318 | 6,054 | 963 | 2,378 | **7,196** | 811 | 959 | 743 | Tortoise ORM |
| Insert: Batch | 11,460 | **15,173** | 640 | 11,594 | 14,674 | 479 | 1,025 | 446 | peewee |
| Insert: Bulk | 22,416 | **37,593** | 784 | — | 34,248 | 999 | 1,993 | 595 | peewee |
| Filter: Large | **165,462** | 90,441 | 47,522 | 82,871 | 158,489 | 40,063 | 17,435 | 38,255 | Django |
| Filter: Small | 62,596 | 47,163 | 17,561 | 76,098 | **79,925** | 21,654 | 8,506 | 22,694 | Tortoise ORM |
| Get | 7,721 | 8,114 | 2,860 | **18,681** | 8,993 | 2,323 | 2,130 | 3,650 | SQLObject |
| Filter: dict | 207,814 | 115,182 | 29,339 | — | **247,155** | 51,369 | 48,807 | 45,120 | Tortoise ORM |
| Filter: tuple | 218,169 | 115,580 | 46,677 | — | **237,584** | 50,876 | 51,575 | 64,276 | Tortoise ORM |
| Update: Whole | 10,886 | 14,309 | 602 | **31,423** | 20,118 | 1,138 | 1,118 | 779 | SQLObject |
| Update: Partial | 12,619 | 20,456 | 777 | **52,465** | 25,682 | 1,442 | 1,135 | 796 | SQLObject |
| Delete | 2,680 | **28,103** | 362 | 2,472 | 20,670 | 1,114 | 1,113 | 788 | peewee |
| **Geometric Mean** | 22,624 | 29,186 | 3,114 | 18,418 | **38,276** | 3,958 | 3,772 | 3,473 | **Tortoise ORM** |

### Test 3: Wide Model (32+ fields)

![SQLite Test 3](images/sqlite_test3.png)

| Operation | Django | peewee | SA ORM async | SQLObject | Tortoise ORM | Piccolo | ormar | SQLModel | Best |
|-----------|--------|--------|--------------|-----------|--------------|---------|-------|----------|------|
| Insert: Single | 2,021 | **3,661** | 778 | 1,912 | 2,165 | 783 | 574 | 736 | peewee |
| Insert: Batch | 6,182 | 6,638 | 636 | 5,903 | **7,752** | 639 | 442 | 573 | Tortoise ORM |
| Insert: Bulk | 8,705 | **14,058** | 1,467 | — | 12,293 | 1,233 | 1,177 | 699 | peewee |
| Filter: Large | **50,491** | 31,874 | 11,281 | 44,508 | 44,768 | 8,448 | 2,169 | 11,641 | Django |
| Filter: Small | 29,980 | 17,509 | 12,006 | **41,667** | 28,139 | 6,583 | 1,908 | 9,970 | SQLObject |
| Get | 4,200 | 2,706 | 2,798 | **10,627** | 6,039 | 1,656 | 723 | 2,574 | SQLObject |
| Filter: dict | **64,349** | 42,897 | 11,465 | — | 50,009 | 11,879 | 5,346 | 10,259 | Django |
| Filter: tuple | **70,890** | 45,657 | 10,093 | — | 48,596 | 12,978 | 4,926 | 12,255 | Django |
| Update: Whole | 5,865 | 3,596 | 618 | **24,904** | 12,475 | 1,129 | 768 | 464 | SQLObject |
| Update: Partial | 11,289 | 21,407 | 773 | **45,538** | 24,997 | 1,124 | 1,422 | 371 | SQLObject |
| Delete | 14,027 | **29,225** | 778 | 2,270 | 27,356 | 1,148 | 1,416 | 774 | peewee |
| **Geometric Mean** | 13,594 | 13,284 | 2,346 | 12,437 | **16,920** | 2,362 | 1,386 | 1,941 | **Tortoise ORM** |

---

## Analysis

### PostgreSQL — Async ORMs dominate

Tortoise ORM and Piccolo share the top spots. Both use `asyncpg`, which provides binary protocol encoding and connection pooling — a massive advantage over `psycopg2`-based sync ORMs. Piccolo leads on simple reads (Filter: dict/tuple) thanks to its ultra-thin result mapping layer, while Tortoise excels at writes (Insert, Update, Delete) and wins overall on the more complex Test 2 and Test 3 schemas.

### MySQL — Tortoise ORM leads decisively

Tortoise ORM wins every test by a wide margin (2x over the runner-up). The `asyncmy` driver (native async MySQL protocol) outperforms both `aiomysql` and sync `mysqlclient`/`pymysql`. SA ORM async is competitive on reads but falls behind on writes. Piccolo does not support MySQL.

### SQLite — Sync ORMs are faster

On SQLite, async overhead hurts more than it helps — there is no concurrency to exploit due to SQLite's single-writer lock. Sync ORMs (peewee, Django, SQLObject) avoid the `aiosqlite` polling overhead and win handily. peewee takes the overall crown, with Django dominating large filter operations and SQLObject excelling at single-row operations (Get, Update). Tortoise ORM remains the fastest async ORM on SQLite.

### Key takeaways

- **For PostgreSQL/MySQL production workloads**: Tortoise ORM and Piccolo (PG only) offer the best throughput
- **For SQLite/local development**: peewee and Django are faster due to lower async overhead
- **SA ORM async / SQLModel**: Strong on reads but consistently slow on writes due to Session/UoW overhead. SQLModel tracks closely with SA ORM async (expected — it's a thin wrapper around SQLAlchemy)
- **ormar**: Pydantic validation overhead causes significant slowdown, especially on wide models (Test 3)
- **SQLObject**: Missing bulk insert and dict/tuple filter operations, but surprisingly fast on single-row SQLite operations

## Running the benchmarks

```sh
# Clone and install
git clone https://github.com/tortoise/orm-benchmarks.git
cd orm-benchmarks
uv venv && source .venv/bin/activate
uv pip install -e .

# SQLite (default)
cd benchmarks && sh bench.sh

# PostgreSQL
export DBTYPE=postgres PASSWORD=yourpassword PGPORT=5432
cd benchmarks && sh bench.sh

# MySQL
export DBTYPE=mysql PASSWORD=yourpassword MYPORT=3306
cd benchmarks && sh bench.sh
```
