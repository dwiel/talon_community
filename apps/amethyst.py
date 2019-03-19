import os
import json

from talon import ui, resource
from talon.voice import Key, Context

from .. import utils

ctx = Context(
    "amethyst", func=lambda app, win: bool(ui.apps(bundle="com.amethyst.Amethyst"))
)

keymap = {
    # "window next screen": Key("ctrl-alt-shift-l"),
    # "window (previous|prev) screen": Key("ctrl-alt-shift-h"),
    "window next": Key("alt-shift-j"),
    "window previous": Key("alt-shift-k"),
    "window move desk": Key("ctrl-alt-shift-h"),
    "window full": Key("alt-shift-d"),
    "window tall": Key("alt-shift-a"),
    "window middle": Key("alt-shift-`"),
    "window move main": Key("alt-shift-enter"),
    "window grow": Key("alt-shift-l"),
    "window shrink": Key("alt-shift-h"),
    "window reevaluate": Key('alt-shift-z'),
}

screen_mapping = {"1": "w", "2": "e", "3": "r", "4": "q"}
keymap.update(
    {
        "window screen %s" % name: Key("ctrl-alt-shift-%s" % screen_mapping[name])
        for name in screen_mapping.keys()
    }
)

ctx.keymap(keymap)
