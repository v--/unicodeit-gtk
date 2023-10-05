from __future__ import annotations
from types import FrameType
import signal
import warnings

import unicodeit
from unicodeit.data import REPLACEMENTS
from setproctitle import setproctitle

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GObject, GLib, Adw, Gtk, Gdk, Pango  # noqa: E402


class UnicodeItExitCodeError(Exception):
    code: int

    def __init__(self, code: int):
        self.code = code

    def __str__(self):
        return f'The GUI exited with code {self.code}'


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


class UnicodeItContent(Gtk.Box):
    submit_button: Gtk.Button
    input_widget: UnicodeItInput
    output_widget: UnicodeItOutput

    def __init__(self):
        super().__init__()

        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(10)
        self.set_size_request(400, 100)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        self.input_widget = UnicodeItInput()
        self.input_widget.connect('changed', self.on_input)
        self.input_widget.connect('activate', self.on_enter)
        self.append(self.input_widget)

        self.output_widget = UnicodeItOutput()
        self.append(self.output_widget)

        self.submit_button = Gtk.Button.new_with_label('Submit')
        self.submit_button.connect('clicked', self.on_enter)
        self.append(self.submit_button)

    def on_input(self, widget: UnicodeItInput):
        self.output_widget.set_text(unicodeit.replace(widget.get_text()))

    def on_enter(self, widget: Gtk.Widget):
        self.emit('submit', self.output_widget.get_text())
        self.input_widget.reset_text()


GObject.signal_new(
    'submit',
    UnicodeItContent,
    0,
    GObject.TYPE_NONE,
    [GObject.TYPE_STRING]
)


class UnicodeItApp(Adw.Application):
    hide_window: bool
    window: Adw.ApplicationWindow | None
    toolbar: Adw.ToolbarView  # type: ignore
    header: Adw.HeaderBar
    outer_container: Gtk.CenterBox
    inner_container: Gtk.CenterBox
    key_control: Gtk.EventControllerKey
    content: UnicodeItContent

    def __init__(self, hide_window: bool):
        super().__init__(application_id='net.ivasilev.UnicodeItGTK')
        GLib.set_application_name('Unicode it')
        setproctitle('unicodeit-gtk')
        signal.signal(signal.SIGUSR1, self.show_window)

        self.hide_window = hide_window
        self.toolbar = Adw.ToolbarView()  # type: ignore
        self.outer_container = Gtk.CenterBox()
        self.inner_container = Gtk.CenterBox()
        self.content = UnicodeItContent()
        self.key_control = Gtk.EventControllerKey()

    def run(self, args: list[str] | None):
        exit_status = super().run(args)

        if exit_status > 0:
            raise UnicodeItExitCodeError(exit_status)

    def do_activate(self):
        self.window = Adw.ApplicationWindow(application=self, title='Unicode it')
        self.window.set_content(self.toolbar)

        self.header = Adw.HeaderBar()
        self.toolbar.add_top_bar(self.header)

        self.outer_container.set_orientation(Gtk.Orientation.VERTICAL)
        self.toolbar.set_content(self.outer_container)

        self.outer_container.set_center_widget(self.inner_container)
        self.inner_container.set_center_widget(self.content)

        self.key_control.connect('key-pressed', self.on_key_press)
        self.window.add_controller(self.key_control)

        self.window.present()

        # Showing the window and then hiding it prevents a delay on the first trigger
        if self.hide_window:
            self.window.set_visible(False)

    def on_key_press(
        self,
        key: Gtk.EventControllerKey,
        key_value: int,
        key_code: int,
        state: Gdk.ModifierType
    ):
        if key_value == Gdk.KEY_Escape:
            self.content.emit('submit', '')

    def show_window(self, sig_num: int, stack_frame: FrameType | None):
        if self.window:
            self.window.set_visible(True)
