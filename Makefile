.PHONY: format
format:
	echo "Format"
	poetry run black src
	poetry run isort src

.PHONY: lint
lint:
	echo "Lint"
	poetry run isort --check --diff src
	poetry run black --check --diff src
	poetry run flake8 src
