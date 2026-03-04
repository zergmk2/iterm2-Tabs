.PHONY: help install install-dev test lint format clean run dist release bump-version

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make <target>\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-15s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install:  ## Install the package
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -e ".[dev]"
	pre-commit install

run:  ## Run the application
	python -m iterm2_tabs

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=iterm2_tabs --cov-report=html

lint:  ## Run linting
	ruff check src/ tests/
	mypy src/

format:  ## Format code
	black src/ tests/
	ruff check --fix src/ tests/

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name '*.app' -prune -exec rm -rf {} +

check: lint test  ## Run all checks (lint + test)

dist:  ## Build macOS .app bundle
	@echo "Building iterm2-tabs.app..."
	@./scripts/build_app.sh
	@echo "✓ Built dist/iterm2-tabs.app"

bump-version:  ## Bump version number (usage: make bump-version VERSION=0.1.0)
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is required. Usage: make bump-version VERSION=0.1.0"; \
		exit 1; \
	fi
	@./scripts/bump-version.sh $(VERSION)

release:  ## Create a new release (usage: make release VERSION=0.1.0)
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is required. Usage: make release VERSION=0.1.0"; \
		exit 1; \
	fi
	@./scripts/release.sh v$(VERSION)

