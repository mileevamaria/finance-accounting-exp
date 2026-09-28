.PHONY: help install sync run lint format check test \
	revision upgrade downgrade current history shell

UV := uv
ALEMBIC := $(UV) run alembic

help:
	@echo "Available commands:"
	@echo "  make sync                 Install/sync dependencies"
	@echo "  make run                  Run FastAPI"
	@echo "  make lint                 Run Ruff"
	@echo "  make format               Format code"
	@echo "  make check                Ruff check + format check"
	@echo "  make test                 Run tests"
	@echo "  make revision m='msg'     Create migration"
	@echo "  make upgrade              Apply migrations"
	@echo "  make downgrade            Roll back one migration"
	@echo "  make current              Show current migration"
	@echo "  make history              Show migration history"
	@echo "  make shell                Open Python shell"

sync:
	$(UV) sync

run:
	$(UV) run uvicorn app.main:app --reload

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

check:
	$(UV) run ruff check .
	$(UV) run ruff format --check .

test:
	$(UV) run pytest

revision:
	$(ALEMBIC) revision --autogenerate -m "$(m)"

upgrade:
	$(ALEMBIC) upgrade head

downgrade:
	$(ALEMBIC) downgrade -1

current:
	$(ALEMBIC) current

history:
	$(ALEMBIC) history

shell:
	$(UV) run python
