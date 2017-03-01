import os

decoder_command_keys = [
    "DELAY",
    "SPACE",
    "CTRL",
    "ALT",
    "GUI",
    "WINDOWS",
    "ESC",
    "ESCAPE",
    "PRINTSCREEN",
    "INSERT",
    "HOME",
    "DELETE",
    "END",
    "ENTER",
    "PAGEUP",
    "PAGEDOWN",
    "LEFTARROW",
    "LEFT",
    "DOWNARROW",
    "DOWN",
    "RIGHTARROW",
    "RIGHT",
    "UPARROW",
    "UP",
    "SCROLLLOCK",
    "WINDOWS",
    "MENU",
    "TAB",
    "CAPSLOCK",
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
    "F10",
    "F11",
    "F12",
    "GUI R",
    "GUI D",
    "CTRL-ALT",
    "CTRL-SHIFT",
    "ALT-SHIFT"
    "CONTROL",
    "ESCAPE",
    "DELAY",
    "DEFAULTDELAY",
    "DEFAULT_DELAY",
    "CTRL S",
    "CTRL V",
    "CTRL X",
    "CTRL Z",
    "CTRL C",
    "ALT F4",
    "WAKE",
    "SLEEP",
    "APP",
    "STOP",
    "POWER"
    ]


def list_languages():
    languages = []
    lang_dir = os.path.join(os.path.dirname(__file__), 'languages')
    for filename in os.listdir(lang_dir):
        if filename.endswith('.json'):
            languages.append(filename)
    return languages


def convert_hex(int_value):
    encoded = format(int_value, '02x')

    return encoded
