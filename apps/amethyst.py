from talon import cron, ui
from talon.voice import Context, Key, press


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
            if event[:4] == "win_" and arg.app.name in ("Amethyst", "loginwindow"):
                return
            if event[:4] == "app_" and arg.name in (
                "AddressBookSourceSync",
                "Google Software Update",
                "CoreServicesUIAgent",
                "AddressBookManager",
                "loginwindow",
            ):
                return
            try:
                print(event, arg)
                print(arg.app.name, arg.name)
                print(ui.active_window())
                print(ui.active_window().hidden)
                print()
            except:
                pass
            press("alt-shift-z")
            cron.after("250ms", lambda: press("alt-shift-z"))
            cron.after("250ms", lambda: press("alt-shift-z"))


ui.register("", ui_event)
