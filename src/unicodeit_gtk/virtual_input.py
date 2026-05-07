import subprocess


def type_virtually(string: str) -> None:
    """Enter a string via virtual input.

    The implementation is really underwhelming because it simply invokes wtype.
    I am hoping that a more elegant implementation falls out of thin air,
    but I am reluctant to implement my own hacky input method.
    """
    subprocess.Popen(['wtype', string])
