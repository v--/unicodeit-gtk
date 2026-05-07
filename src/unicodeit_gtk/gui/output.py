from gi.repository import Gtk, Pango


class UnicodeItOutput(Gtk.Label):
    def __init__(self) -> None:
        super().__init__(
            halign=Gtk.Align.START,
            ellipsize=Pango.EllipsizeMode.START,
            margin_start=9,
            single_line_mode=True,
        )

        self.set_text('')

    def set_text(self, text: str) -> None:
        if text:
            super().set_text(text)
            self.remove_css_class('placeholder')
        else:
            super().set_text('(La)TeX code will be rendered here')
            self.add_css_class('placeholder')

