import warnings

from gi.repository import Gtk

from .completion import UnicodeItCompletion


class UnicodeItInput(Gtk.Entry):
    completion: UnicodeItCompletion

    def __init__(self) -> None:
        super().__init__()
        self.add_css_class('content-input')
        self.completion = UnicodeItCompletion()

        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=DeprecationWarning)
            self.set_completion(self.completion)

    def reset_text(self) -> None:
        return self.get_buffer().set_text('', 0)

    def get_text(self) -> str:
        return self.get_buffer().get_text()
