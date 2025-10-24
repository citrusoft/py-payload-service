# Makefile for fastapi-server local dev tasks

COMPOSE=docker-compose -f docker-compose.yml

.PHONY: up down build create-db logs

up:
	$(COMPOSE) up -d --build app

down:
	$(COMPOSE) down -v

build:
	$(COMPOSE) build --no-cache app

logs:
	$(COMPOSE) logs -f app

# create-db: start only the DB, wait until it's ready, then run the create_db script
create-db:
	@echo "Starting database..."
	$(COMPOSE) up -d db
	@echo "Waiting for Postgres to be ready..."
	@set -e; \
	for i in `seq 1 30`; do \
		$(COMPOSE) exec -T db pg_isready -U payload_user >/dev/null 2>&1 && break || sleep 1; \
	done; \
	echo "Running create_db script inside app container..."; \
	# Mount the repository into the container at /workdir and point PYTHONPATH to /workdir/src
	$(COMPOSE) run --rm -e PYTHONPATH=/workdir/src -v $$(pwd):/workdir app python /workdir/create_db_safe.py
	@echo "create-db finished"
