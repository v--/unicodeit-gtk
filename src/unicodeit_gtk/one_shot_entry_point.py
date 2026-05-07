import sys

from setproctitle import setproctitle

from unicodeit_gtk.virtual_input import type_virtually

from .gui import UnicodeItApp


def on_submit(app: UnicodeItApp, value: str) -> None:
    if value:
        type_virtually(value)


def one_shot_entry_point() -> None:
    setproctitle('unicodeit-gtk')

    app = UnicodeItApp(one_shot=True)
    app.connect('submit', on_submit)
    app.run(sys.argv)
