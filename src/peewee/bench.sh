#!/bin/sh

cd $(dirname $0)

# setup DB
rm -f /dev/shm/db.sqlite3
python -m set_up

# Test A → Insert
python -m test_a

# Test B → Transactioned Intsert
python -m test_b

# Test C → Bulk Insert
python -m test_c

# Test D → Filter on level
python -m test_d

# Test E → Search in text
python -m test_e

# Test F → Filter limit 20
python -m test_f

# Test G → Get
python -m test_g

# teardown DB
rm -f /dev/shm/db.sqlite3

