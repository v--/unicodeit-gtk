import signal

from gi.repository import Adw, Gio, GLib, GObject

from .window import UnicodeItWindow


class UnicodeItApp(Adw.Application):
    window: UnicodeItWindow | None
    one_shot: bool

    def __init__(self, one_shot: bool = False) -> None:
        super().__init__(application_id='net.ivasilev.UnicodeItGTK')
        self.one_shot = one_shot
        self.window = None

        GLib.set_application_name('Unicode it')
        GLib.unix_signal_add(
            GLib.PRIORITY_DEFAULT,
            signal.SIGUSR1,
            self.activate_window,
        )

        self.set_accels_for_action('app.minimize', ['Escape'])
        self.connect('activate', self.on_activate)

    def on_activate(self, app: 'UnicodeItApp') -> None:
        self.window = UnicodeItWindow(application=self)
        self.window.connect('submit', self.on_submit)

        minimize_action = Gio.SimpleAction(name='minimize')
        minimize_action.connect('activate', self.on_minimize)
        self.add_action(minimize_action)

    def on_submit(self, window: UnicodeItWindow, value: str) -> None:
        self.emit('submit', value)

        if self.one_shot and self.window:
            self.window.close()

    def on_minimize(self, action: Gio.Action, parameter: None) -> None:
        if self.one_shot:
            if self.window:
                self.window.close()
        elif self.window:
            self.window.minimize()

    def activate_window(self) -> bool:
        if self.window:
            self.window.activate()

        return GLib.SOURCE_CONTINUE


GObject.signal_new(
    'submit',
    UnicodeItApp,
    0,
    GObject.TYPE_NONE,
    [GObject.TYPE_STRING],
)
