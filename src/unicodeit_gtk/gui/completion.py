import warnings

from gi.repository import Gtk
from unicodeit.data import REPLACEMENTS


class UnicodeItCompletion(Gtk.EntryCompletion):
    store: Gtk.ListStore

    def __init__(self) -> None:
        super().__init__()
        self.store = Gtk.ListStore(str)

        for key, _ in REPLACEMENTS:
            self.store.append([key])

        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=DeprecationWarning)
            self.set_text_column(0)
            self.set_model(self.store)
