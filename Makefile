# Career Advisor Backend Makefile
.PHONY: help test test-verbose test-coverage test-all install install-all migrate migrate-up migrate-down migrate-status migrate-all-up migrate-all-down run dev clean lint format

# Service names
SERVICES := conversations-service prompts-service users-service

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "  test-all               - Run tests for all services"
	@echo "  dev                   - Start server in development mode (Tilt)"
	@echo "  clean                 - Clean cache and temporary files"
	@echo "  lint                  - Run code linting"
	@echo "  format                - Format code with black"
	@echo ""

test-all:
	@echo "Running tests for all services..."
	@for service in $(SERVICES); do \
		if [ -d "microservices/services/$$service" ]; then \
			echo "Testing $$service..."; \
			cd microservices/services/$$service && .venv/bin/python -m pytest src/tests/ || exit 1; \
			cd - > /dev/null; \
		else \
			echo "Warning: Service $$service not found, skipping..."; \
		fi; \
	done
	@echo "All tests completed successfully!"

dev:
	tilt up

# Code quality
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	.venv/bin/python -m flake8 microservices/

format:
	.venv/bin/python -m black microservices/
