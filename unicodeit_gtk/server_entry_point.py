import subprocess
import sys

from setproctitle import setproctitle

from unicodeit_gtk import UnicodeItApp, apply_styling


def on_activate(app: UnicodeItApp):
    if app.window:
        app.window.minimize()


def on_submit(app: UnicodeItApp, value: str):
    if value:
        subprocess.Popen(['wtype', value])


def server_entry_point():
    setproctitle('unicodeit-gtk')
    apply_styling()

    app = UnicodeItApp()
    app.connect('submit', on_submit)
    app.connect('activate', on_activate)
    app.run(sys.argv)
