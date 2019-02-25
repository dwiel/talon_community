from os import system

from talon.voice import Context, Key, press
from ..utils import parse_words_as_integer

ctx = Context("window_control")


def jump_tab(m):
    tab_number = parse_words_as_integer(m._words[1:])
    if tab_number != None and tab_number > 0 and tab_number < 9:
        press("cmd-%s" % tab_number)


ctx.keymap(
    {
        # tab control
        "(open | new) tab": Key("cmd-t"),
        "close tab": Key("cmd-w"),
        "([switch] tab (right | next) | goneck)": Key("cmd-shift-]"),
        "([switch] tab (left | previous | preev) | gopreev)": Key("cmd-shift-["),
        "[switch] tab (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8)": jump_tab,
        "[switch] tab (end | rightmost)": Key("cmd-9"),
        # zooming
        "zoom in": Key("cmd-="),
        "zoom out": Key("cmd--"),
        "zoom normal": Key("cmd-0"),
        # window control
        "(open | new) window": Key("cmd-n"),
        "window close": Key("cmd-shift-w"),
        "([switch] window (next | right) | gibby)": Key("cmd-`"),
        "([switch] window (left | previous | preev) | shibby)": Key("cmd-shift-`"),
        "[switch] space (right | next)": Key("ctrl-right"),
        "[switch] space (left | previous | preev)": Key("ctrl-left"),
        "(minimise window | curtail)": Key("cmd-m"),
        "show app windows": Key("ctrl-down"),
        # application navigation
        "[open] launcher": Key("cmd-space"),
        "([switch] app (next | right) | swick)": Key("cmd-tab"),
        "[switch] app (left | previous | preev)": Key("cmd-shift-tab"),
        "[open] mission control": lambda m: system("open -a 'Mission Control'"),
    }
)
