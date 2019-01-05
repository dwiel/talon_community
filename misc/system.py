from talon.voice import Context, Key

ctx = Context("system")

ctx.keymap(
    {
        "(prefies | preferences)": Key("cmd-,"),
        "put computer to sleep": lambda m: os.system("pmset sleepnow"),
    }
)
