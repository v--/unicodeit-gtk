import signal
import warnings

import unicodeit
from unicodeit.data import REPLACEMENTS

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GObject, GLib, Adw, Gtk, Gio, Pango  # noqa: E402


class UnicodeItCompletion(Gtk.EntryCompletion):
    store: Gtk.ListStore

    def __init__(self):
        super().__init__()
        self.store = Gtk.ListStore(str)

        for (key, value) in REPLACEMENTS:
            self.store.append([key])

        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=DeprecationWarning)
            self.set_text_column(0)
            self.set_model(self.store)


class UnicodeItInput(Gtk.Entry):
    completion: UnicodeItCompletion

    def __init__(self):
        super().__init__()
        self.add_css_class('content-input')
        self.completion = UnicodeItCompletion()

        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=DeprecationWarning)
            self.set_completion(self.completion)

    def reset_text(self):
        return self.get_buffer().set_text('', 0)

    def get_text(self):
        return self.get_buffer().get_text()


class UnicodeItOutput(Gtk.Label):
    def __init__(self):
        super().__init__(
            halign=Gtk.Align.START,
            ellipsize=Pango.EllipsizeMode.START,
            margin_start=9,
            single_line_mode=True
        )

        self.set_text('')

    def set_text(self, text: str):
        if text:
            super().set_text(text)
            self.remove_css_class('placeholder')
        else:
            super().set_text('(La)TeX code will be rendered here')
            self.add_css_class('placeholder')


class UnicodeItWindow(Adw.ApplicationWindow):
    toolbar: Adw.ToolbarView  # type: ignore
    header: Adw.HeaderBar
    input_widget: UnicodeItInput
    output_widget: UnicodeItOutput

    def __init__(self, application: Gtk.Application):
        super().__init__(application=application, title='Unicode it')

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

    def get_rendered_text(self):
        return unicodeit.replace(self.input_widget.get_text())

    def on_input(self, widget: UnicodeItInput):
        self.output_widget.set_text(self.get_rendered_text())

    def on_enter(self, widget: Gtk.Widget):
        text = self.get_rendered_text()
        self.minimize()
        self.emit('submit', text)

    def minimize(self):
        self.set_visible(False)
        self.input_widget.reset_text()

    def activate(self):
        self.present()


GObject.signal_new(
    'submit',
    UnicodeItWindow,
    0,
    GObject.TYPE_NONE,
    [GObject.TYPE_STRING]
)


class UnicodeItApp(Adw.Application):
    window: UnicodeItWindow | None

    def __init__(self):
        super().__init__(application_id='net.ivasilev.UnicodeItGTK')
        self.window = None

        GLib.set_application_name('Unicode it')
        GLib.unix_signal_add(
            GLib.PRIORITY_DEFAULT,
            signal.SIGUSR1,
            self.activate_window
        )

        self.set_accels_for_action('app.minimize', ['Escape'])
        self.connect('activate', self.on_activate)

    def run(self, args: list[str] | None):
        exit_status = super().run(args)

        if exit_status > 0:
            raise SystemExit(exit_status)

    def on_activate(self, app: 'UnicodeItApp'):
        self.window = UnicodeItWindow(application=self)
        self.window.connect('submit', self.on_submit)

        minimize_action = Gio.SimpleAction(name='minimize')
        minimize_action.connect('activate', self.on_minimize)
        self.add_action(minimize_action)

    def on_submit(self, window: UnicodeItWindow, value: str):
        self.emit('submit', value)

    def on_minimize(self, action: Gio.Action, parameter: None):
        if self.window:
            self.window.minimize()

    def activate_window(self):
        if self.window:
            self.window.activate()

        return GLib.SOURCE_CONTINUE


GObject.signal_new(
    'submit',
    UnicodeItApp,
    0,
    GObject.TYPE_NONE,
    [GObject.TYPE_STRING]
)
