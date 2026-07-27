SHELL := bash
.SHELLFLAGS := -e -x -c

# Cross-platform Bash
ifeq ($(OS),Windows_NT)
BASH := "C:/Program Files/Git/bin/bash.exe"
else
BASH := bash
endif

.PHONY: install
install: ## 🚀 Set up environment and install project
	@echo "🚀 Syncing dependencies with uv..."
	@if [ -f uv.lock ]; then \
		uv sync --frozen; \
	else \
		uv sync; \
	fi
	@echo "🔧 Installing project in editable mode..."
	uv pip install -e .

.PHONY: check-version
check-version:
	@echo "🔍 Checking the release tag against the package version..."
	@VERSION=$$(uv run hatch version); \
	EXPECTED_TAG="v$$VERSION"; \
	if [ -z "$(RELEASE_TAG)" ]; then \
	    echo "❌ RELEASE_TAG must identify the release being checked."; \
	    exit 1; \
	elif [ "$(RELEASE_TAG)" != "$$EXPECTED_TAG" ]; then \
	    echo "❌ Release tag '$(RELEASE_TAG)' does not match package version '$$VERSION'."; \
	    exit 1; \
	else \
	    echo "✅ Release tag matches package version: $(RELEASE_TAG)"; \
	fi

.PHONY: check-dev-version
check-dev-version:
	@echo "🔍 Checking the computed development version..."
	@VERSION=$$(uv run hatch version); \
	if [[ "$$VERSION" =~ \.dev[0-9]+$$ ]]; then \
	    echo "✅ Development version: $$VERSION"; \
	else \
	    echo "❌ Expected a development version, got: $$VERSION"; \
	    exit 1; \
	fi

.PHONY: check
check: ## Run all code quality checks
	@echo "🚀 Checking lock file consistency"
	@if [ -f uv.lock ]; then \
		uv lock --locked; \
	else \
		uv lock; \
	fi
	@echo "🚀 Running pre-commit hooks"
	uv run pre-commit run --all-files

.PHONY: test
test: ## Run tests using tox
	@echo "🚀 Testing code: Running tox across Python versions"
	uv run tox

.PHONY: test-local
test-local: ## Run tests in current Python environment using uv
	@echo "🚀 Testing code locally"
{%- if cookiecutter.codecov == "y" %}
	uv run python -m pytest -rvx tests --cov --cov-config=pyproject.toml --cov-report html:coverage-html
{%- else %}
	uv run python -m pytest -rvx tests
{%- endif %}

.PHONY: build
build: clean ## Build package using uv
	@echo "🚀 Building project"
	uv build

.PHONY: clean
clean: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	rm -rf dist build *.egg-info
	rm -rf .coverage coverage-html coverage.xml .pytest_cache
	find . -name '*.pyc' -delete

.PHONY: version
version: ## Print the current project version
	uv run hatch version

.PHONY: tag
tag: ## 🏷 Tag the current release version (fixes changelog and pushes tag)
	$(BASH) scripts/tag_release.sh

.PHONY: check-dist
check-dist: ## Validate dist/ artifacts (long description, format)
	@echo "🔍 Validating dist/ artifacts..."
	uv run twine check dist/*

.PHONY: publish
publish: ## Publish to production PyPI
	@echo "🚀 Publishing to PyPI"
	UV_PUBLISH_TOKEN=$(PYPI_TOKEN) uv publish --publish-url=https://upload.pypi.org/legacy/ --no-cache

.PHONY: publish-test
publish-test: ## Publish to TestPyPI (for dry runs)
	@echo "🚀 Publishing to TestPyPI"
	UV_PUBLISH_TOKEN=$(TEST_PYPI_TOKEN) uv publish --publish-url=https://test.pypi.org/legacy/ --no-cache

.PHONY: build-and-publish
build-and-publish: build check-dist publish ## Build and publish in one step

.PHONY: help
help:
	uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
