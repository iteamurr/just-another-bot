.PHONY: format_all

format_all: ## Run formatters and linters
	poetry run ruff format .
	poetry run ruff check --fix .
