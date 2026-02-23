import subprocess
import sys

from setproctitle import setproctitle

from .app import UnicodeItApp
from .styling import apply_styling


def on_submit(app: UnicodeItApp, value: str):
    if value:
        subprocess.Popen(['wtype', value])


def one_shot_entry_point():
    setproctitle('unicodeit-gtk')
    apply_styling()

    app = UnicodeItApp(one_shot=True)
    app.connect('submit', on_submit)
    app.run(sys.argv)
