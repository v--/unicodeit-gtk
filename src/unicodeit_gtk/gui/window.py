import unicodeit
from gi.repository import Adw, GObject, Gtk

from .input import UnicodeItInput
from .output import UnicodeItOutput


class UnicodeItWindow(Adw.ApplicationWindow):
    toolbar: Adw.ToolbarView  # type: ignore
    header: Adw.HeaderBar
    input_widget: UnicodeItInput
    output_widget: UnicodeItOutput

    def __init__(self, application: Gtk.Application) -> None:
        super().__init__(
            application=application,
            title='Unicode it',
            height_request=-1,  # Force minimal height
        )

        self.toolbar = Adw.ToolbarView()  # type: ignore
        self.set_content(self.toolbar)

        self.header = Adw.HeaderBar()
        self.toolbar.add_top_bar(self.header)

        self.content = Gtk.Grid()
        self.content.add_css_class('content')
        self.toolbar.set_content(self.content)

        self.output_widget = UnicodeItOutput()
        self.content.attach(self.output_widget, column=0, row=0, width=1, height=1)

        self.input_widget = UnicodeItInput()
        self.input_widget.connect('changed', self.on_input)
        self.input_widget.connect('activate', self.on_enter)
        self.content.attach(self.input_widget, column=0, row=1, width=1, height=1)

        self.activate()

    def get_rendered_text(self) -> str:
        return unicodeit.replace(self.input_widget.get_text())

    def on_input(self, widget: UnicodeItInput) -> None:
        self.output_widget.set_text(self.get_rendered_text())

    def on_enter(self, widget: Gtk.Widget) -> None:
        text = self.get_rendered_text()
        self.minimize()
        self.emit('submit', text)

    def minimize(self) -> None:
        self.set_visible(False)
        self.input_widget.reset_text()

    def activate(self) -> bool:
        self.present()
        return True


GObject.signal_new(
    'submit',
    UnicodeItWindow,
    0,
    GObject.TYPE_NONE,
    [GObject.TYPE_STRING],
)
