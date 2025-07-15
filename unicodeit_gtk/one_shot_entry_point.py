import subprocess
import sys

from setproctitle import setproctitle

from unicodeit_gtk import UnicodeItApp, apply_styling


def on_submit(app: UnicodeItApp, value: str):
    if value:
        subprocess.Popen(['wtype', value])

    if app.window:
        app.window.close()


def one_shot_entry_point():
    setproctitle('unicodeit-gtk')
    apply_styling()

    app = UnicodeItApp()
    app.connect('submit', on_submit)
    app.run(sys.argv)
