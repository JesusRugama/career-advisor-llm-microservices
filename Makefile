# Career Advisor Backend Makefile
.PHONY: help test test-verbose test-coverage install migrate migrate-upgrade migrate-downgrade run dev clean lint format

# Default target
help:
	@echo "Available commands:"
	@echo "  test           - Run all tests"
	@echo "  test-verbose   - Run all tests with verbose output"
	@echo "  test-coverage  - Run tests with coverage report"
	@echo "  install        - Install dependencies"
	@echo "  migrate        - Create new migration"
	@echo "  migrate-up     - Run migrations (upgrade)"
	@echo "  migrate-down   - Rollback migrations (downgrade)"
	@echo "  run            - Start the FastAPI server"
	@echo "  dev            - Start server in development mode"
	@echo "  clean          - Clean cache and temporary files"
	@echo "  lint           - Run code linting"
	@echo "  format         - Format code with black"

# Testing commands
test:
	.venv/bin/python -m pytest src/

test-verbose:
	.venv/bin/python -m pytest src/ -v

test-coverage:
	.venv/bin/python -m pytest src/ --cov=src --cov-report=term-missing

# Development setup
install:
	.venv/bin/python -m pip install -r requirements.txt

# Database commands
migrate:
	.venv/bin/python -m alembic revision --autogenerate -m "$(msg)"

migrate-up:
	.venv/bin/python -m alembic upgrade head

migrate-down:
	.venv/bin/python -m alembic downgrade -1

# Server commands
run:
	.venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

dev:
	.venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Code quality
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	.venv/bin/python -m flake8 src/

format:
	.venv/bin/python -m black src/
