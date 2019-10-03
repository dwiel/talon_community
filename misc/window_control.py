from os import system

from talon.voice import Context, Key, press
from talon import macos
from ..utils import parse_words_as_integer

ctx = Context("window_control")


def jump_tab(m):
    tab_number = parse_words_as_integer(m._words[1:])
    if tab_number is not None and tab_number > 0 and tab_number < 9:
        press("cmd-%s" % tab_number)


ctx.keymap(
    {
        # tab control
        "(open | new) tab": Key("cmd-t"),
        "close tab": Key("cmd-w"),
        "([switch] tab (right | next))": Key("cmd-shift-]"),
        "([switch] tab (left | previous | preev))": Key("cmd-shift-["),
        "[switch] tab (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8)": jump_tab,
        "[switch] tab (end | rightmost)": Key("cmd-9"),
        # zooming
        "zoom in": Key("cmd-="),
        "zoom out": Key("cmd--"),
        "zoom normal": Key("cmd-0"),
        # window control
        "(open | new) window": Key("cmd-n"),
        "close window": Key("cmd-shift-w"),
        "([switch] window (next | right) | gibby)": Key("cmd-`"),
        "([switch] window (left | previous | preev) | shibby)": Key("cmd-shift-`"),
        "[switch] space (right | next)": Key("ctrl-right"),
        "[switch] space (left | previous | preev)": Key("ctrl-left"),
        "(minimise window | curtail)": Key("cmd-m"),
        "([show] (app | application) windows | expozay)": lambda m: macos.dock_notify(
            "com.apple.expose.front.awake"
        ),
        "quit it": Key("cmd-q"),
        # application navigation
        "[open] launcher": Key("cmd-space"),
        "([switch] app (next | right) | swick)": Key("cmd-tab"),
        "[switch] app (left | previous | preev)": Key("cmd-shift-tab"),
        "[open] mission control": lambda m: macos.dock_notify("com.apple.expose.awake"),
        "[open] launchpad": lambda m: macos.dock_notify("com.apple.launchpad.toggle"),
        # the following requires keyboard shortcut for mission control in System Preferences > Keyboard > Shortcuts > Mission Control > Show Notification Center.
        # is there a bundle id we can use instead?
        "([(open | show)] notification center | ( (show | open) (today | widgets) ))": Key(
            "shift-ctrl-f8"
        ),
    }
)
