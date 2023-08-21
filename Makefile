.PHONY: fmt
fmt:
	poetry run black src tests examples
	poetry run isort src tests examples

.PHONY: lint
lint:
	poetry run isort --check --diff src tests examples
	poetry run black --check --diff src tests examples
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

.PHONY: notion-e2e
install:
	poetry run python examples/create_notion_page.py
	poetry run python examples/create_notion_page_from_template_with_value.py
	poetry run python examples/create_notion_page_from_template.py
