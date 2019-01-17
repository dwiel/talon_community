from talon.voice import Key, Context

ctx = Context('iterm', bundle='com.googlecode.iterm2')

keymap = {
    'broadcaster': Key('cmd-alt-i'),
    'split horizontal': Key('cmd-shift-d'),
    'split vertical': Key('cmd-d'),
    'password': Key('cmd-alt-f'),
}

ctx.keymap(keymap)
