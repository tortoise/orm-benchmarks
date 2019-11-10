#!/bin/sh

cd $(dirname $0)

# setup DB
../db.sh
PYTHONPATH="." sqlobject-admin create -m models

# Test A → Insert
python -m test_a

# Test B → Transactioned Intsert
python -m test_b

# Test C → Bulk Insert
# Not available

# Test D → Filter on level
python -m test_d

# Test E → Filter limit 20
python -m test_e

# Test F → Get
python -m test_f

# Test I → Update full
python -m test_i

# Test I → Update full
python -m test_j

# Test K → Delete
python -m test_k
