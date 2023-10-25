.PHONY: lint

lint:
	poetry run ruff check unicodeit_gtk bin/*
	poetry run mypy --package unicodeit_gtk
	poetry run mypy bin/unicodeit-gtk-server
	poetry run mypy bin/unicodeit-gtk
