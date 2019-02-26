from talon.voice import Key, press, Str, Context

# Commands for annotating pdfs.

ctx = Context("skim", bundle="net.sourceforge.skim-app.skim")

keymap = {"highlight": Key("cmd-ctrl-h"), "anchor": Key("cmd-alt-n")}

ctx.keymap(keymap)
