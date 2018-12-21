from talon import ui
from talon.voice import Key, Context

single_digits = "0123456789"
NAMED_DESKTOPS = {digit: int(digit) for digit in single_digits}
NAMED_DESKTOPS.update({
    # "gmail": 1,
    # "slack": 2,
})

ctx = Context(
    "amethyst", func=lambda app, win: bool(ui.apps(bundle="com.amethyst.Amethyst"))
)

keymap = {
    # 'desk <dgndictation>': desk,
    "window next screen": Key("ctrl-alt-shift-l"),
    "window (previous|prev) screen": Key("ctrl-alt-shift-h"),
    "window next": Key("alt-shift-j"),
    "window previous": Key("alt-shift-k"),
    "window move desk": Key("ctrl-alt-shift-h"),
    "window full": Key("alt-shift-d"),
    "window tall": Key("alt-shift-a"),
    "window middle": Key("alt-shift-`"),
    "window move main": Key("alt-shift-enter"),
    "window grow": Key("alt-shift-l"),
    "window shrink": Key("alt-shift-h"),
}

keymap.update(
    {
        "desk %s" % name: Key("ctrl-%s" % NAMED_DESKTOPS[name])
        for name in NAMED_DESKTOPS.keys()
    }
)

keymap.update(
    {
        "window move desk %s" % name: Key("ctrl-alt-shift-%s" % NAMED_DESKTOPS[name])
        for name in NAMED_DESKTOPS.keys()
    }
)

screen_mapping = {"1": "w", "2": "e", "3": "r", "4": "t"}
keymap.update(
    {"window screen %s" % name: Key("ctrl-alt-shift-%s" % name) for name in "1234"}
)

ctx.keymap(keymap)
