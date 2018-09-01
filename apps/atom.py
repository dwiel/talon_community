import time

from talon.voice import Key, press, Str, Context, Rule
from ..misc import std
from ..utils import parse_words_as_integer, parse_words, numeral_map, numerals, optional_numerals, text

ctx = Context('atom', bundle='com.github.atom')

atom_hotkey = 'cmd-shift-ctrl-alt-t'
atom_command_pallet = 'cmd-shift-p'

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

# NB! These command names are duplicated in commands.js
COMMANDS = Struct(
    DELETE_TO_BOL = 'b',
    DELETE_TO_EOL = 'e',
    SELECT_LINES = 's',
    FIND_NEXT = 'f',
    FIND_PREVIOUS = 'p',
    COPY_LINE = 'c',
    MOVE_LINE = 'm',
)

############## support for parsing numbers as command postfix

def text_to_number(m):

    tmp = [str(s).lower() for s in m._words]
    words = [parse_word(word) for word in tmp]

    result = 0
    factor = 1
    for word in reversed(words):
        if word not in numerals:
            # we consumed all the numbers and only the command name is left.
            break

        result = result + factor * int(numeral_map[word])
        factor = 10 * factor

    return result

def text_to_number_wrapper(func):
    def wrapper(*args, **kwargs):
        if not kwargs and len(args) == 1:
            if isinstance(args[0], Rule):
                args = (text_to_number(args[0]),) + args[1:]
        func(*args, **kwargs)

    return wrapper

def parse_word(word):
    word = word.lstrip('\\').split('\\', 1)[0]
    return word


######### actions and helper functions
@text_to_number_wrapper
def jump_to_bol(line):
    press('ctrl-g')
    Str(str(line))(None)
    press('enter')

def jump_to_end_of_line():
    press('cmd-right')

def jump_to_beginning_of_text():
    press('cmd-left')

def jump_to_nearly_end_of_line():
    press('left')

def jump_to_bol_and(then):
    def fn(m):
        if len(m._words) > 1:
            jump_to_bol(m)
        else:
            press('ctrl-a')
            press('cmd-left')
        then()
    return fn

def jump_to_eol_and(then):
    def fn(m):
        if len(m._words) > 1:
            jump_to_bol(m)
        press('cmd-right')
        then()
    return fn

def toggle_comments(*unneeded):
   press('cmd-/')

def snipline():
    press('ctrl-shift-k')

def get_first_word(m):
    return str(m.dgndictation[0]._words[0])

def execute_atom_command(command, parameters=None):
    press(atom_hotkey)
    press(command)
    if parameters:
        Str(parameters)(None)
        press('enter')

def find_next(m):
    execute_atom_command(COMMANDS.FIND_NEXT, get_first_word(m))

def find_previous(m):
    execute_atom_command(COMMANDS.FIND_PREVIOUS, get_first_word(m))

def copy_line(m):
    line = text_to_number(m)
    execute_atom_command(COMMANDS.COPY_LINE, str(line))

def move_line(m):
    line = text_to_number(m)
    execute_atom_command(COMMANDS.MOVE_LINE, str(line))

def select_lines(m):
    # NB: line_range is e.g. 99102, which is parsed in
    #  the atom package as lines 99..102
    line_range = text_to_number(m)
    execute_atom_command(COMMANDS.SELECT_LINES, str(line_range))

def cut_line(m):
    jump_to_bol(m)
    press("cmd-left")
    press("shift-down")
    press("cmd-x")


def paste_line(m):
    jump_to_bol(m)
    press("cmd-left")
    press("cmd-v")


def change_pain(m):
    line = text_to_number(m)
    for i in range(10):
        press('cmd-k')
        press('cmd-left')
    for i in range(1, line):
        press('cmd-k')
        press('cmd-right')

def command_from_palette(command):
    press(atom_command_pallet)
    time.sleep(0.25)
    Str(command)(None)
    time.sleep(0.25)
    press('enter')

def command(command):
    def function(m):
        command_from_palette(command)
    return function

def jump_tab(m, tab_number=None):
    if tab_number is None:
        tab_number = parse_words_as_integer(m._words[1:])

    if tab_number != None and tab_number > 0 and tab_number < 10:
        press('cmd-%s'%tab_number)

def close_tab(m, tab_number=None):
    if tab_number is None:
        tab_number = parse_words_as_integer(m._words[2:])

    if tab_number != None and tab_number > 0 and tab_number < 10:
        press('cmd-%s'%tab_number)
        press('cmd-w')

snippets = {
    'define function': 'definefunction',
    'define method': 'definemethod',
    'define command': 'definecommand',
    'define class': 'class',
    'doc string': 'docstring',
    'for loop': 'forloop',
    'print': 'print',
    'import': 'import',
    'from': 'from',
    'list': 'list',
    'dictionary': 'dict',
    'if name main': 'ifnamemain',
    'if name main main': 'ifnamemainmain',
}

def code_snippet(m):
    words = ' '.join([str(word).lower() for word in m._words[1:]])
    Str(snippets[words])(None)
    press('tab')

def code_snippet_naked(m):
    words = ' '.join([str(word).lower() for word in m._words[0:]])
    Str(snippets[words])(None)
    press('tab')

keymap = {
    'sprinkle' + optional_numerals: jump_to_bol,
    'spring' + optional_numerals: jump_to_eol_and(jump_to_beginning_of_text),
    '(dear | sprinkler)' + optional_numerals: jump_to_eol_and(lambda: None),
    'smear' + optional_numerals: jump_to_eol_and(jump_to_nearly_end_of_line),
    'trundle': toggle_comments,
    'trundle' + numerals: jump_to_bol_and(toggle_comments),
    'jolt': Key('cmd-x cmd-v cmd-v'),

    'snipline' + optional_numerals: jump_to_bol_and(snipline),
    'cut line' + optional_numerals: cut_line,
    'paste line' + optional_numerals: paste_line,


    # 'snipple': [Key(atom_hotkey), Key(COMMANDS.DELETE_TO_BOL)],
    # 'snipper': [Key(atom_hotkey), Key(COMMANDS.DELETE_TO_EOL)],

    '(copy line | clonesert)' + numerals: copy_line,
    'move line' + numerals: move_line,

    'crew <dgndictation>': find_next,
    'trail <dgndictation>': find_previous,

    'shackle': Key('cmd-l'),
    'selrang' + numerals: select_lines,

    'shockey': Key('cmd-shift-enter'),
    'shockoon': Key('cmd-right enter'),
    'sprinkoon' + numerals: jump_to_eol_and(lambda: press('enter')),

    'peach': Key('cmd-t'),
    'peach <dgndictation>': [Key('cmd-t'), text],
    'peachy <dgndictation>': [Key('cmd-t'), text, Key('enter')],
    'advanced open file': Key('cmd-alt-o'),
    'pain' + numerals: change_pain,
    'tab' + numerals: jump_tab,
    'close tab' + numerals: close_tab,
    '(reopen | unclose) tab': Key('cmd-shift-t'),
    'split pain left': [Key('cmd-k'), Key('left')],
    'split pain right': [Key('cmd-k'), Key('right')],
    'split pain up': [Key('cmd-k'), Key('up')],
    'split pain down': [Key('cmd-k'), Key('down')],
    'mark all': Key('cmd-shift-f'),

    'command pallet': Key(atom_command_pallet),
    'cursor center': command('center-line:toggle'),
    'cursor top': [command('center-line:toggle'), command('center-line:toggle')],
    # 'cell pair': command('py-ast-edit:select-parent'),
    'cell expand': Key('alt-up'),
    'cell contract': Key('alt-down'),
    'cell this': command('py-ast-edit:select-this'),

    # needs bracket-matcher atom package; still a bit poor.
    'bracken': command('bracket-matcher:select-inside-bracket'),
    'go match': command('bracket-matcher:go-to-matching-bracket'),
    'remove matching brackets': command('bracket-matcher:remove-matching-brackets'),

    'quinn' + '({})'.format(' | '.join(snippets.keys())): code_snippet,
    # '({})'.format(' | '.join(snippets.keys())): code_snippet_naked,

    # python
    'quinn if': ['if :', Key('left')],
    'else': ['else:', Key('enter')],
    'self': 'self',
    'to do': '# TODO: ',
}

ctx.keymap(keymap)
