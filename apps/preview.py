from talon.voice import Key, press, Str, Context
# Commands for annotating pdfs.

ctx = Context('preview', bundle='com.apple.Preview')

keymap = {
    'highlight': Key('cmd-ctrl-h'),
    'note': Key('cmd-ctrl-n'),
}

ctx.keymap(keymap)
