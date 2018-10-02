#!/bin/sh

cd $(dirname $0)

# setup DB
export DJANGO_SETTINGS_MODULE="simple.settings"
rm -f db.sqlite3
./manage-simple.py migrate -v 0

# Test A → Insert
python -m simple.test_a

# Test B → Transactioned Intsert
python -m simple.test_b

# Test C → Bulk Insert
python -m simple.test_c

# Test D → Filter on level
python -m simple.test_d

# Test E → Search in text
python -m simple.test_e

# Test F → Filter limit 20
python -m simple.test_f

# Test G → Get
python -m simple.test_g

# teardown DB
#rm -f db.sqlite3

