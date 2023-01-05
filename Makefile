.PHONY: fmt
fmt:
	poetry run black src
	poetry run isort src

.PHONY: lint
lint:
	poetry run isort --check --diff src
	poetry run black --check --diff src
	poetry run flake8 src

.PHONY: test
test:
	poetry run pytest tests/ --cov=autonote --cov-report=xml

.PHONY: docs
docs:
	poetry run make html --directory docs/

.PHONY: install
install:
	poetry install
