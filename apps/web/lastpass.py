from talon.voice import Context, Key


context = Context(
    "lastpass",
    func=lambda app, win: app.bundle in ["com.google.Chrome", "org.mozilla.firefox"],
)

context.keymap(
    {
        "last pass next": Key("cmd-pageup"),
        "last pass (previous | preev)": Key("cmd-pagedown"),
        "last pass generate password": Key("cmd-shift-ctrl-alt-1"),
        "last pass recheck page": Key("cmd-shift-ctrl-alt-2"),
        "last pass site search": Key("cmd-shift-ctrl-alt-3"),
        "last pass submit": Key("cmd-shift-ctrl-alt-4"),
        "last pass open vault": Key("cmd-shift-ctrl-alt-5"),
        "last pass save data": Key("cmd-shift-ctrl-alt-6"),
        "last pass logout": Key("cmd-shift-ctrl-alt-7"),
        "last pass fill in default": Key("cmd-shift-ctrl-alt-8"),
    }
)
