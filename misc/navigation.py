from talon.voice import Context, Key

ctx = Context("navigation")


keymap = {
    # scrolling
    "scroll down": [Key("down")] * 30,
    "scroll up": [Key("up")] * 30,
    # NB home and end do not work in all apps
    "(scroll way down | doomway)": Key("cmd-down"),
    "(scroll way up | jeepway)": Key("cmd-up"),
    "page up": [Key("pageup")],
    "page down": [Key("pagedown")],
}

ctx.keymap(keymap)
