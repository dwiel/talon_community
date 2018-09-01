from talon.voice import Key, Context

ctx = Context('amethyst')

keymap = {
    # 'desk <dgndictation>': desk,

    'window next screen': Key('ctrl-alt-shift-l'),
    'window (previous|prev) screen': Key('ctrl-alt-shift-h'),
    'window next': Key('alt-shift-j'),
    'window previous': Key('alt-shift-k'),
    'window move desk': Key('ctrl-alt-shift-h'),

    'window full': Key('alt-shift-d'),
    'window tall': Key('alt-shift-a'),
    'window middle': Key('alt-shift-`'),
    'window move main': Key('alt-shift-enter'),
    'window grow': Key('alt-shift-l'),
    'window shrink': Key('alt-shift-h'),
}

single_digits = '0123456789'
keymap.update({'desk %s' % digit: Key('ctrl-%s' % digit) for digit in single_digits})
keymap.update({'window move desk %s' % digit: Key('ctrl-alt-shift-%s' % digit) for digit in single_digits})

screen_mapping = {
    '1': 'w',
    '2': 'e',
    '3': 'r',
    '4': 't',
}
keymap.update({'window screen %s' % digit: Key('ctrl-alt-shift-%s' % digit) for digit in '1234'})

ctx.keymap(keymap)
