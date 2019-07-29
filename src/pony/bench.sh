#!/bin/sh

cd $(dirname $0)

# setup DB
rm -f /dev/shm/db.sqlite3

# Test A → Insert
python -m test_a

# Test B → Transactioned Intsert
python -m test_b

# Test C → Bulk Insert
# Not supported

# Test D → Filter on level
python -m test_d

# Test E → Filter limit 20
python -m test_e

# Test F → Get
python -m test_f

# Test G → dict
python -m test_g

# Test H → tuple
python -m test_h

# teardown DB
rm -f /dev/shm/db.sqlite3

