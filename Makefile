.PHONY: fmt
fmt:
	uv run --locked ruff check --fix src tests examples
	uv run --locked ruff format src tests examples/*.py

.PHONY: lint
lint:
	uv run --locked ruff check src tests examples
	uv run --locked ruff format --check src tests examples/*.py

.PHONY: test
test:
	uv run --locked pytest tests/ --cov=autonote --cov-report=xml

.PHONY: docs
docs:
	uv run --locked make html --directory docs/

.PHONY: install
install:
	uv sync --locked --all-groups

.PHONY: e2e-notion
e2e-notion:
	uv run --locked python examples/create_notion_page.py
	uv run --locked python examples/create_notion_page_from_template.py
	uv run --locked python examples/create_notion_page_from_template_with_value.py
	uv run --locked python examples/create_notion_page_from_template_with_value_content.py

.PHONY: build
build:
	uv build
