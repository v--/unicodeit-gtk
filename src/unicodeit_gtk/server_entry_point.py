import sys

from setproctitle import setproctitle

from unicodeit_gtk.virtual_input import type_virtually

from .gui import UnicodeItApp


def on_activate(app: UnicodeItApp) -> None:
    if app.window:
        app.window.minimize()


def on_submit(app: UnicodeItApp, value: str) -> None:
    if value:
        type_virtually(value)


def server_entry_point() -> None:
    setproctitle('unicodeit-gtk')

    app = UnicodeItApp()
    app.connect('submit', on_submit)
    app.connect('activate', on_activate)
    app.run(sys.argv)
