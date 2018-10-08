from talon.voice import Context, Key

ctx = Context("jupyter")

ctx.keymap({"cell run": Key("shift-enter")})
