from __future__ import annotations
import signal
import warnings

import unicodeit
from unicodeit.data import REPLACEMENTS
from setproctitle import setproctitle

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GObject, GLib, Adw, Gtk, Gio, Pango  # noqa: E402


GUI_WIDTH = 500
GUI_SPACING = 15


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
        super().__init__()
        self.set_ellipsize(Pango.EllipsizeMode.START)
        self.set_halign(Gtk.Align.START)
        self.set_margin_start(9)
        self.set_text('')

    def set_text(self, text: str):
        if text:
            super().set_text(text)
        else:
            self.set_markup(
                '<span foreground="gray">(La)TeX code will be rendered here</span>'
            )


class UnicodeItWindow(Adw.ApplicationWindow):
    toolbar: Adw.ToolbarView  # type: ignore
    header: Adw.HeaderBar
    input_widget: UnicodeItInput
    output_widget: UnicodeItOutput

    def __init__(self, application: Gtk.Application):
        super().__init__(application=application, title='Unicode it')
        self.set_size_request(GUI_WIDTH, -1)

        self.toolbar = Adw.ToolbarView()  # type: ignore
        self.set_content(self.toolbar)

        self.header = Adw.HeaderBar()
        self.toolbar.add_top_bar(self.header)

        self.content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=GUI_SPACING,
            margin_top=GUI_SPACING,
            margin_bottom=GUI_SPACING,
            margin_start=GUI_SPACING,
            margin_end=GUI_SPACING
        )

        self.toolbar.set_content(self.content)

        self.output_widget = UnicodeItOutput()
        self.content.append(self.output_widget)

        self.input_widget = UnicodeItInput()
        self.input_widget.connect('changed', self.on_input)
        self.input_widget.connect('activate', self.on_enter)
        self.content.append(self.input_widget)

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
        setproctitle('unicodeit-gtk')
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

    def on_activate(self, app: UnicodeItApp):
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
