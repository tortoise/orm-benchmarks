checkfiles = benchmarks/
black_opts = -l 100 -t py38
PASSWORD ?= "123456"
PGPORT ?= 5433

deps:
	@uv pip install -e .

style: deps
	isort $(checkfiles)
	black $(black_opts) $(checkfiles)

check: deps
	black --check $(black_opts) $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	flake8 $(checkfiles)
	bandit -r $(checkfiles)

benchmark_all: deps
	cd benchmarks && PASSWORD=$(PASSWORD) PGPORT=$(PGPORT) sh bench_all.sh

benchmark_sqlite: deps
	cd benchmarks && PASSWORD=$(PASSWORD) DBTYPE=sqlite sh bench.sh

benchmark_mysql: deps
	cd benchmarks && PASSWORD=$(PASSWORD) DBTYPE=mysql sh bench.sh

benchmark_postgres: deps
	cd benchmarks && PASSWORD=$(PASSWORD) PGPORT=$(PGPORT) DBTYPE=postgres sh bench.sh
