#!/bin/sh

export ITERATIONS=10000

printf '' > outfile

django/bench.sh | tee -a outfile
peewee/bench.sh | tee -a outfile
pony/bench.sh | tee -a outfile
#sqlalchemy/bench.sh
#sqlobject/bench.sh
#tortoise/bench.sh

cat outfile | ./present.py

rm -f outfile
