from talon.voice import Context, Key
from os import system
from talon.voice import Context, Key

ctx = Context('navigation')

keymap = {
    # Requires activation of System Preferences -> Shortcuts -> Input Sources
    # -> "Select the previous input source"
    'change language': Key('ctrl-space'),

    # Application navigation
    'swick': Key('cmd-tab'),
    # 'totch': Key('cmd-w'),
    'new window': Key('cmd-n'),
    '(next window | gibby)': Key('cmd-`'),
    '(last window | shibby)': Key('cmd-shift-`'),
    'next space': Key('cmd-alt-ctrl-right'),
    'last space': Key('cmd-alt-ctrl-left'),

    # Following three commands should be application specific
    #'(baxley | go back)': Key('cmd-alt-left'),
    #'(fourthly | go forward)': Key('cmd-alt-right'),
    # '(new tab | peach)': Key('cmd-t'),

    # deleting
    # '(delete line)': Key('cmd-right cmd-backspace'),
    'steffi': Key('alt-ctrl-backspace'),
    'stippy': Key('alt-ctrl-delete'),
    'carmex': Key('alt-backspace'),
    'kite': Key('alt-delete'),
    'snipple': Key('cmd-shift-left delete'),
    'snipper': Key('cmd-shift-right delete'),
    'slurp': Key('backspace delete'),
    'slurpies': Key('alt-backspace alt-delete'),

    # moving
    '(tab | tarp)': Key('tab'),
    'tarsh': Key('shift-tab'),
    # 'slap': [Key('cmd-right enter')],
    'shocker': [Key('cmd-left enter up')],
    'wonkrim': Key('alt-ctrl-left'),
    'wonkrish': Key('alt-ctrl-right'),
    'fame': Key('alt-left'),
    'fish': Key('alt-right'),
    'ricky': Key('cmd-right'),
    'ricky 2': [Key('cmd-right'), Key('cmd-right')],
    'ricky 3': [Key('cmd-right'), Key('cmd-right'), Key('cmd-right')],
    'ricky 4': [Key('cmd-right'), Key('cmd-right'), Key('cmd-right'), Key('cmd-right')],
    'lefty': Key('cmd-left'),
    'lefty 2': [Key('cmd-left'), Key('cmd-left')],
    'lefty 3': [Key('cmd-left'), Key('cmd-left'), Key('cmd-left')],
    'lefty 4': [Key('cmd-left'), Key('cmd-left'), Key('cmd-left'), Key('cmd-left')],
    'crimp': Key('left'),
    'crimp 2': [Key('left'), Key('left')],
    'crimp 3': [Key('left'), Key('left'), Key('left')],
    'crimp 4': [Key('left'), Key('left'), Key('left'), Key('left')],
    'crimp 5': [Key('left'), Key('left'), Key('left'), Key('left'), Key('left')],
    'chris': Key('right'),
    'chris 2': [Key('right'), Key('right')],
    'chris 3': [Key('right'), Key('right'), Key('right')],
    'chris 4': [Key('right'), Key('right'), Key('right'), Key('right')],
    'chris 5': [Key('right'), Key('right'), Key('right'), Key('right'), Key('right')],
    '(up | jeep)': Key('up'),
    '(down | dune | doom)':  Key('down'),

    'scroll down': [Key('down')] * 30,
    '(doomway | scroll way down)': Key('cmd-down'),
    'scroll up': [Key('up')] * 30,
    '(jeepway | scroll way up)': Key('cmd-up'),

    # selecting
    'shreepway': Key('cmd-shift-up'),
    'shroomway': Key('cmd-shift-down'),
    'shreep': Key('shift-up'),
    'shroom': Key('shift-down'),
    'scram': Key('alt-shift-left'),
    'scrish': Key('alt-shift-right'),
    '(schrim | shift left)': Key('shift-left'),
    '(shrish | shift right)': Key('shift-right'),

    # Application navigation
    'launcher': Key('cmd-space'),
    'swick': Key('cmd-tab'),

    'close tab': Key('cmd-w'),
    'close window': Key('cmd-shift-w'),

    'mission': lambda m: system('open -a \'Mission Control\''),
    'show windows': Key('ctrl-down'),
    'curtail': Key('cmd-m'),

    '(next window | gibby)': Key('cmd-`'),
    '(last window | shibby)': Key('cmd-shift-`'),
    'window space right': Key('cmd-alt-ctrl-right'),
    'window space left': Key('cmd-alt-ctrl-left'),

    'new window': Key('cmd-n'),

    # 'next app': Key('cmd-tab'),
    # 'last app': Key('cmd-shift-tab'),

    'next space': Key('cmd-alt-ctrl-right'),
    'last space': Key('cmd-alt-ctrl-left'),

    # Following three commands should be application specific
    'last tab': Key('cmd-shift-['),
    'next tab': Key('cmd-shift-]'),
    'new tab': Key('cmd-t'),
    'reload': Key('cmd-r'),

    # 'scroll down': [Key('down')] * 30,
    'page up': [Key('pageup')],
    # 'scroll up': [Key('up')] * 30,
    'page down': [Key('pagedown')],
    # 'scroll top': [Key('cmd-up')],
    # 'scroll bottom': [Key('cmd-down')],

    # deleting
    'junk': Key('backspace'),
    'scrap': Key('delete'),
    'kite': Key('alt-delete'),
    'snip left': Key('cmd-shift-left delete'),
    'snip right': Key('cmd-shift-right delete'),
    'slurp': Key('backspace delete'),
    'trough': Key('alt-backspace'),

    # moving
    # '(tab | tarp)': Key('tab'),
    'tarp': Key('tab'),
    'tarsh': Key('shift-tab'),
    'slap': [Key('cmd-right enter')],
    'peg': Key('alt-left'),
    'fran': Key('alt-right'),
    'ricky': Key('cmd-right'),
    'derek': Key('cmd-right space'),
    'lefty': Key('cmd-left'),
    'jeep': Key('up'),
    'lloyd':  Key('left'),
    'chris': Key('right'),
    'doom':  Key('down'),
    'doom way': Key('cmd-down'),
    'jeep way': Key('cmd-up'),

    # zooming
    'zoom in': Key('cmd-='),
    'zoom out': Key('cmd--'),
    'zoom normal': Key('cmd-0'),

    # selecting
    'select all': Key('cmd-a'),
    'snatch': Key('cmd-x'),
    'shackle': [Key('cmd-left'), Key('shift-cmd-right')],
    'stoosh': Key('cmd-c'),
    'spark': Key('cmd-v'),
    'shreepway': Key('cmd-shift-up'),
    'shroomway': Key('cmd-shift-down'),
    'shreep': Key('shift-up'),
    'shroom': Key('shift-down'),
    'lecksy': Key('cmd-shift-left'),
    'ricksy': Key('cmd-shift-right'),
    'shlocky': Key('alt-shift-left'),
    'shrocky': Key('alt-shift-right'),
    'shlicky': Key('shift-left'),
    'shricky': Key('shift-right'),
}

ctx.keymap(keymap)
