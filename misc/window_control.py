import os

from talon.voice import Context, Key

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
        "next tab": Key("cmd-shift-]"),
        "((last | previous | preev) tab | gopreev)": Key("cmd-shift-["),
        "tab (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8)": jump_tab,
        "(end | rightmost) tab": Key("cmd-9"),
        # zooming
        "zoom in": Key("cmd-="),
        "zoom out": Key("cmd--"),
        "zoom normal": Key("cmd-0"),
        # window control
        "new window": Key("cmd-n"),
        "close window": Key("cmd-shift-w"),
        "(next window | gibby)": Key("cmd-`"),
        "(last window | shibby)": Key("cmd-shift-`"),
        "(window space right | next space)": Key("ctrl-right"),
        "(window space left | last space)": Key("ctrl-left"),
        "curtail": Key("cmd-m"),
        # Application navigation
        "launcher": Key("cmd-space"),
        "(next app | swick)": Key("cmd-tab"),
        "last app": Key("cmd-shift-tab"),
        "mission": lambda m: system("open -a 'Mission Control'"),
        "show windows": Key("cmd-down"),
    }
)
