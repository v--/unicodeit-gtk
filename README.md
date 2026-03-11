# Unicode it GTK

[![AUR Package](https://img.shields.io/aur/version/unicodeit-gtk)](https://aur.archlinux.org/packages/unicodeit-gtk)

This is a GTK IME popup for entering symbols via (La)TeX - a simple wrapper around the [unicodeit Python library](https://github.com/svenkreiss/unicodeit).

![Basic screenshot](./screenshot_basic.png)

There is basic completion implemented:

![Basic autocomplete](./screenshot_autocomplete.png)

A benefit of using GTK is that emoji can be entered via "Ctrl+.":

![Emoji screenshot](./screenshot_emoji.png)

## Usage

The project provides a `unicodeit-gtk` executable, which launches the popup window seen on the screenshots above.

* `Escape` hides the window.
* `Enter` inputs the corresponding Unicode characters via [wtype](https://github.com/atx/wtype)

Since starting a GTK application is not instantaneous, an alternative is provided by another command --- `unicodeit-gtk-server`. Once started, the server will listen to SIGUSR1 and then a window will pop up. This can be useful when the following command is bound to a keyboard shortcut:

    pkill -SIGUSR1 unicodeit-gtk

## Installation

An easy way to install both executables for the current user is via [`uv`](https://docs.astral.sh/uv/):

    uv tool install unicodeit-gtk --from git+https://github.com/v--/unicodeit-gtk

Other tools like [`pipx`](https://pipx.pypa.io/) can also be used - simply run the following from the cloned repository:

    uv sync
    uv build --wheel
    pipx install --include-deps dist/*.whl

The hard prerequisites are a supported version of Python and GTK4.

> [!TIP]
> An [AUR package](https://aur.archlinux.org/packages/unicodeit-gtk) is available for reference, as well as a [GitHub Action](./.github/workflows/lint.yaml). If you are packaging this for some other package manager, consider using PEP-517 tools as shown in [this PKGBUILD file](https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=unicodeit-gtk).
