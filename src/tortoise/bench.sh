#!/bin/sh

cd $(dirname $0)

# setup DB
rm -f /dev/shm/db.sqlite3
# run regular loop benchmarks
python -m bench

# setup DB
rm -f /dev/shm/db.sqlite3
# run uvloop benchmarks
UVLOOP=1 python -m bench

# teardown DB
rm -f /dev/shm/db.sqlite3
