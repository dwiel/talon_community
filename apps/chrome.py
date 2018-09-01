import time

from ..utils import parse_words_as_integer

from talon.voice import Context, Key, Str, press

# It is recommended to use this script in tandem with Vimium, a Google Chrome plugin for controlling the browser via keyboard
# https://vimium.github.io/

context = Context('GoogleChrome', bundle='com.google.Chrome')


def open_focus_devtools(m):
    press('cmd-shift-c')


def show_panel(name):
    open_focus_devtools(None)

    # Open command menu
    press('cmd-shift-p')

    Str('Show %s' % (name))(None)
    press('enter')


def next_panel(m):
    open_focus_devtools(None)
    press('cmd-]')


def last_panel(m):
    open_focus_devtools(None)
    press('cmd-[')


def focus_address_bar(m):
    press('cmd-l')


# Return focus from the devtools to the page
def refocus_page(m):
    focus_address_bar(None)
    time.sleep(0.1)
    # Escape button
    # This leaves the focus on the page at previous tab focused point, not the beginning of the page
    press('escape')


def back(m):
    refocus_page(None)
    press('cmd-left')
    refocus_page(None)


def forward(m):
    refocus_page(None)
    press('cmd-]')
    refocus_page(None)


def jump_tab(m):
    tab_number = parse_words_as_integer(m._words[1:])
    if tab_number != None and tab_number > 0 and tab_number < 9:
        press('cmd-%s' % tab_number)


context.keymap({
    '(address bar | focus address | focus url | url)':
    focus_address_bar,
    'copy url':
    'yy',
    'back[ward]':
    back,
    'forward':
    forward,
    'reload':
    Key('cmd-r'),
    'hard reload':
    Key('cmd-shift-r'),
    'new tab':
    Key('cmd-t'),
    'close tab':
    Key('cmd-w'),
    '(reopen | unclose) tab':
    Key('cmd-shift-t'),
    'next tab':
    Key('cmd-alt-right'),
    '(last | prevous | preev) tab':
    Key('cmd-alt-left'),
    'tab (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8)':
    jump_tab,
    '(end | rightmost) tab':
    Key('cmd-9'),
    'find':
    Key('cmd-f'),
    'next':
    Key('cmd-g'),
    '(last | prevous)':
    Key('cmd-shift-g'),
    'toggle dev tools':
    Key('cmd-alt-i'),
    'command [menu]':
    Key('cmd-shift-p'),
    'next panel':
    next_panel,
    '(last | prevous) panel':
    last_panel,
    'show application [panel]':
    lambda m: show_panel('Application'),
    'show audit[s] [panel]':
    lambda m: show_panel('Audits'),
    'show console [panel]':
    lambda m: show_panel('Console'),
    'show element[s] [panel]':
    lambda m: show_panel('Elements'),
    'show memory [panel]':
    lambda m: show_panel('Memory'),
    'show network [panel]':
    lambda m: show_panel('Network'),
    'show performance [panel]':
    lambda m: show_panel('Performance'),
    'show security [panel]':
    lambda m: show_panel('Security'),
    'show source[s] [panel]':
    lambda m: show_panel('Sources'),
    '(refocus | focus) page':
    refocus_page,
    '[refocus] dev tools':
    open_focus_devtools,

    # Clipboard
    'cut':
    Key('cmd-x'),
    'copy':
    Key('cmd-c'),
    'paste':
    Key('cmd-v'),
    'paste same style':
    Key('cmd-alt-shift-v'),
    'mendeley':
    Key('cmd-shift-m'),
})
