from talon.voice import Context, Key, press, Str
from ..utils import parse_words_as_integer, repeat_function, optional_numerals

context = Context('VSCode', bundle='com.microsoft.VSCode')

def jump_to_line(m):
    line_number = parse_words_as_integer(m._words[1:])

    if line_number == None:
        return

    # Zeroth line should go to first line
    if line_number == 0:
        line_number = 1

    press('cmd-g')
    Str(str(line_number))(None)
    press('enter')

def jump_tabs(m):
    line_number = parse_words_as_integer(m._words[1:])

    if line_number == None:
        return

    for i in range(0, line_number):
        press('cmd-alt-right')

def jump_to_next_word_instance(m):
    press('escape')
    press('cmd-f')
    Str(' '.join([str(s) for s in m.dgndictation[0]._words]))(None)
    press('return')

def select_lines_function(m):
    divider = 0
    for word in m._words:
        if str(word) == 'until':
            break
        divider += 1
    line_number_from = int(str(parse_words_as_integer(m._words[2:divider])))
    line_number_until = int(str(parse_words_as_integer(m._words[divider+1:])))
    number_of_lines = line_number_until - line_number_from

    press('cmd-g')
    Str(str(line_number_from))(None)
    press('enter')
    for i in range(0, number_of_lines+1):
        press('shift-down')

context.keymap({
    # Selecting text
    'select line' + optional_numerals + 'until' + optional_numerals: select_lines_function,

    # Finding text
    'find': Key('cmd-f'),
    'find next <dgndictation>': jump_to_next_word_instance,

    # Clipboard
    'clone': Key('alt-shift-down'),
    
    # Navigation
    'line' + optional_numerals: jump_to_line,
    'Go to line': Key('cmd-g'),
    'line up' + optional_numerals: repeat_function(2, 'alt-up'),
    'line down' + optional_numerals: repeat_function(2, 'alt-down'),

    # tabbing
    'stiffy': Key('cmd-alt-left'),
    'next tab': Key('cmd-alt-right'),
    'stippy': Key('cmd-alt-right'),
    'last tab': Key('cmd-alt-left'),
    'new tab': Key('cmd-n'),
    'jump' + optional_numerals: jump_tabs,

    # editing
    'bracken': [Key('cmd-shift-ctrl-right')],

    # various
    'comment': Key('cmd-shift-7'),
    'master': Key('cmd-p'),
    'search all': Key('cmd-shift-f'),
    'explorer': Key('cmd-shift-e'),
    '(drop-down | drop)': Key('ctrl-space'),

})