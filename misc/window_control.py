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
        "new tab": Key("cmd-t"),
        "close tab": Key("cmd-w"),
        "(next tab | goneck)": Key("cmd-shift-]"),
        "((previous | preev) tab | gopreev)": Key("cmd-shift-["),
        "tab (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8)": jump_tab,
        "(end | rightmost) tab ": Key("cmd-9"),
        # zooming
        "zoom in": Key("cmd-="),
        "zoom out": Key("cmd--"),
        "zoom normal": Key("cmd-0"),
        # window control
        "new window": Key("cmd-n"),
        "close window": Key("cmd-shift-w"),
        "(next window | gibby)": Key("cmd-`"),
        "((previous | preev) window | shibby)": Key("cmd-shift-`"),
        "(switch space right | next space)": Key("ctrl-right"),
        "(switch space left | (previous | preev) space)": Key("ctrl-left"),
        "(minimise window | curtail)": Key("cmd-m"),
        "show all windows": Key("cmd-down"),
        # application navigation
        "open launcher": Key("cmd-space"),
        "(next app | swick)": Key("cmd-tab"),
        "(previous | preev) app": Key("cmd-shift-tab"),
        "mission control": lambda m: system("open -a 'Mission Control'"),
    }
)
