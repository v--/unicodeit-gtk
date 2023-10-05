.PHONY: lint

lint:
	poetry run ruff check unicodeit_gtk
	poetry run mypy --package unicodeit_gtk
