checkfiles = benchmarks/
black_opts = -l 100 -t py38
PASSWORD ?= "123456"

up:
	@poetry update

deps:
	@poetry install

style: deps
	isort -src $(checkfiles)
	black $(black_opts) $(checkfiles)

check: deps
	black --check $(black_opts) $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	flake8 $(checkfiles)
	bandit -r $(checkfiles)

benchmark_all: deps
	cd benchmarks && PASSWORD=$(PASSWORD) sh bench_all.sh

benchmark_sqlite: deps
	cd benchmarks && PASSWORD=$(PASSWORD) DBTYPE=sqlite sh bench.sh

benchmark_mysql: deps
	cd benchmarks && PASSWORD=$(PASSWORD) DBTYPE=mysql sh bench.sh

benchmark_postgres: deps
	cd benchmarks && PASSWORD=$(PASSWORD) DBTYPE=postgres sh bench.sh
