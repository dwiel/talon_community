import os
import json
import time

from talon import ui, resource
from talon.voice import Key, Context, press

from .. import utils


def amethyst_running():
    return bool(ui.apps(bundle="com.amethyst.Amethyst"))


ctx = Context("amethyst", func=lambda app, win: amethyst_running())

keymap = {
    # "window next screen": Key("ctrl-alt-shift-l"),
    # "window (previous|prev) screen": Key("ctrl-alt-shift-h"),
    "window next": Key("alt-shift-j"),
    "window previous": Key("alt-shift-k"),
    # "window move desk": Key("ctrl-alt-shift-h"),
    "window full": Key("alt-shift-d"),
    "window tall": Key("alt-shift-a"),
    "window middle": Key("alt-shift-`"),
    "window move main": Key("alt-shift-enter"),
    "window grow": Key("alt-shift-l"),
    "window shrink": Key("alt-shift-h"),
    "window reevaluate": Key("alt-shift-z"),
}

screen_mapping = {"1": "w", "2": "e", "3": "r", "4": "q"}
keymap.update(
    {
        "window screen %s" % name: Key("ctrl-alt-shift-%s" % screen_mapping[name])
        for name in screen_mapping.keys()
    }
)

ctx.keymap(keymap)


def ui_event(event, arg):
    if amethyst_running():
        if event in (
            "app_activate",
            "app_launch",
            "app_close",
            "win_open",
            "win_close",
        ):
            if event in ("win_open", "win_closed"):
                if arg.app.name == "Amethyst" or arg.app.name == "loginwindow":
                    return
            if event == "app_activate" and arg.name == "loginwindow":
                return
            print(event, arg)
            press("alt-shift-z")
            time.sleep(0.25)
            press("alt-shift-z")
            time.sleep(0.25)
            press("alt-shift-z")


ui.register("", ui_event)
