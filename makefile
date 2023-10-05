.PHONY: lint

lint:
	poetry run ruff check unicodeit_gtk bin/unicodeit-gtk bin/unicodeit-gtk-daemon
	poetry run mypy --package unicodeit_gtk
	poetry run mypy bin/unicodeit-gtk
	poetry run mypy bin/unicodeit-gtk-daemon
