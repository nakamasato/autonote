.PHONY: fmt
fmt:
	poetry run black src tests
	poetry run isort src tests

.PHONY: lint
lint:
	poetry run isort --check --diff src tests
	poetry run black --check --diff src tests
	poetry run flake8 src tests

.PHONY: test
test:
	poetry run pytest tests/ --cov=autonote --cov-report=xml

.PHONY: docs
docs:
	poetry run make html --directory docs/

.PHONY: install
install:
	poetry install
