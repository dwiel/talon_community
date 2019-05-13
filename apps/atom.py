"""
Make sure to install the talon plugin: https://github.com/tuomassalo/atom-talon
"""

import time
import re

from talon.voice import Key, press, Str, Context, Rule
from ..utils import (
    parse_words_as_integer,
    numeral_map,
    numerals,
    optional_numerals,
    extract_num_from_m,
    text,
)
from .. import utils

ctx = Context("atom", bundle="com.github.atom")

atom_hotkey = "cmd-shift-ctrl-alt-t"
atom_command_pallet = "cmd-shift-p"


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


# NB! These command names are duplicated in commands.js
COMMANDS = Struct(
    DELETE_TO_BOL="b",
    DELETE_TO_EOL="e",
    SELECT_LINES="s",
    FIND_NEXT="f",
    FIND_PREVIOUS="p",
    COPY_LINE="c",
    MOVE_LINE="m",
)

############## support for parsing numbers as command postfix


def parse_word(word):
    word = word.lstrip("\\").split("\\", 1)[0]
    return word


######### actions and helper functions
def jump_to_bol(m):
    if isinstance(m, Rule):
        line = extract_num_from_m(m, default=None)
    else:
        line = m

    if line:
        press("ctrl-g")
        Str(str(line))(None)
        press("enter")


def jump_to_end_of_line():
    press("cmd-right")


def jump_to_beginning_of_text():
    press("cmd-left")


def jump_to_nearly_end_of_line():
    press("left")


def jump_to_bol_and(then):
    def fn(m):
        if len(m._words) > 1:
            jump_to_bol(m)
        else:
            press("ctrl-a")
            press("cmd-left")
        then()

    return fn


def jump_to_eol_and(then):
    def fn(m):
        if len(m._words) > 1:
            jump_to_bol(m)
        press("cmd-right")
        then()

    return fn


def toggle_comments(*unneeded):
    press("cmd-/")


def snipline():
    press("escape")
    press("ctrl-shift-k")


def get_first_word(m):
    return str(m.dgndictation[0]._words[0])


def execute_atom_command(command, parameters=None):
    press(atom_hotkey)
    press(command)
    if parameters:
        Str(parameters)(None)
        press("enter")


def find_next(m):
    execute_atom_command(COMMANDS.FIND_NEXT, get_first_word(m))


def find_previous(m):
    execute_atom_command(COMMANDS.FIND_PREVIOUS, get_first_word(m))


def copy_line(m):
    line = extract_num_from_m(m)
    execute_atom_command(COMMANDS.COPY_LINE, str(line))


def move_line(m):
    line = extract_num_from_m(m)
    execute_atom_command(COMMANDS.MOVE_LINE, str(line))


def select_lines(m):
    # NB: line_range is e.g. 99102, which is parsed in
    #  the atom package as lines 99..102
    line_range = extract_num_from_m(m)
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
    press("up")
    press("cmd-right")
    press("cmd-left")


def change_pain(m):
    line = extract_num_from_m(m)
    for i in range(10):
        press("cmd-k")
        press("cmd-left")
    for i in range(1, line):
        press("cmd-k")
        press("cmd-right")


def command_from_palette(command):
    press(atom_command_pallet)
    time.sleep(0.2)
    utils.paste_text(command)
    time.sleep(0.1)
    press("enter")


def command(command):
    def function(m):
        command_from_palette(command)

    return function


def jump_tab(m, tab_number=None):
    if tab_number is None:
        tab_number = parse_words_as_integer(m._words[1:])

    if tab_number is not None and tab_number > 0 and tab_number < 10:
        press("cmd-%s" % tab_number)


def close_tab(m, tab_number=None):
    if tab_number is None:
        tab_number = parse_words_as_integer(m._words[2:])

    if tab_number is not None and tab_number > 0 and tab_number < 10:
        press("cmd-%s" % tab_number)
        press("cmd-w")


snippets = {
    "define function": "definefunction",
    "define method": "definemethod",
    "define command": "definecommand",
    "define class": "class",
    "doc string": "docstring",
    "for loop": "forloop",
    "print": "print",
    "import": "import",
    "from": "from",
    "list": "list",
    "dictionary": "dict",
    "if name main": "ifnamemain",
    "if name main main": "ifnamemainmain",
}


def code_snippet(m):
    words = " ".join([str(word).lower() for word in m._words[1:]])
    Str(snippets[words])(None)
    press("tab")


def code_snippet_naked(m):
    words = " ".join([str(word).lower() for word in m._words[0:]])
    Str(snippets[words])(None)
    press("tab")


@utils.preserve_clipboard
def duplicate(m):
    press("cmd-x")
    press("cmd-v")
    press("cmd-v")


def replace_spaces_with_tabs(line):
    return line.replace("    ", "\t")


def replace_left_of_equals_with_return(m):
    """
    replace a line containing: a = b
    with                     : return b
    # TODO: create decorator: modify_current_line
    """
    # select line
    press("cmd-l")

    line = utils.copy_selected()
    if "=" not in line:
        return

    m = re.search(r"(\s+).*=(.*)", line)
    print(m.group(1))
    print(m.group(2))
    # line = 'return' + line[line.find('=')+1:]
    line = m.group(1) + "return" + m.group(2) + "\n"
    print(line)

    utils.paste_text(line)
    press("up")


keymap = {
    "sprinkle" + optional_numerals: jump_to_bol,
    # 'spring' + optional_numerals: jump_to_eol_and(jump_to_beginning_of_text),
    "spring" + numerals: jump_to_bol,
    "sprinkler" + optional_numerals: jump_to_eol_and(lambda: None),
    "smear" + optional_numerals: jump_to_eol_and(jump_to_nearly_end_of_line),
    "trundle": toggle_comments,
    "trundle" + numerals: jump_to_bol_and(toggle_comments),
    "indent": Key("cmd-]"),
    "de-dent": Key("cmd-["),
    "jolt": duplicate,
    "snipline" + optional_numerals: jump_to_bol_and(snipline),
    "cut line" + optional_numerals: cut_line,
    "paste line" + optional_numerals: paste_line,
    # 'snipple': [Key(atom_hotkey), Key(COMMANDS.DELETE_TO_BOL)],
    # 'snipper': [Key(atom_hotkey), Key(COMMANDS.DELETE_TO_EOL)],
    "(copy line | clonesert)" + numerals: copy_line,
    "move line" + numerals: move_line,
    "crew <dgndictation>": find_next,
    "trail <dgndictation>": find_previous,
    "replace next": Key("cmd-alt-e"),
    "shackle": Key("cmd-l"),
    "selrang" + numerals: select_lines,
    "shockey": Key("cmd-shift-enter"),
    "shockoon": Key("cmd-right enter"),
    "sprinkoon" + numerals: jump_to_eol_and(lambda: press("enter")),
    "peach": Key("cmd-t"),
    "peach <dgndictation>": [Key("cmd-t"), text],
    "peachy <dgndictation>": [Key("cmd-t"), text, Key("enter")],
    "advanced open file": Key("cmd-alt-o"),
    "(pain | bang)" + numerals: change_pain,
    "tab" + numerals: jump_tab,
    "goneck": Key("cmd-shift-]"),
    "gopreev": Key("cmd-shift-["),
    "close tab" + numerals: close_tab,
    "(reopen | unclose) tab": Key("cmd-shift-t"),
    "split pain left": [Key("cmd-k"), Key("left")],
    "split pain right": [Key("cmd-k"), Key("right")],
    "split pain up": [Key("cmd-k"), Key("up")],
    "split pain down": [Key("cmd-k"), Key("down")],
    "go pain left": [Key("cmd-k"), Key("cmd-left")],
    "go pain right": [Key("cmd-k"), Key("cmd-right")],
    "go pain up": [Key("cmd-k"), Key("cmd-up")],
    "go pain down": [Key("cmd-k"), Key("cmd-down")],
    "(search all files | mark all)": Key("cmd-shift-f"),
    "case sensitive": Key("alt-cmd-c"),
    "command pallet": Key(atom_command_pallet),
    "(cursor | curr) (center | mid)": command("center-line:toggle"),
    "(cursor | curr) top": [
        command("center-line:toggle"),
        command("center-line:toggle"),
    ],
    # 'cell pair': command('py-ast-edit:select-parent'),
    "(cell expand | cell pair)": Key("alt-up"),
    "cell contract": Key("alt-down"),
    "cell this": command("py-ast-edit:select-this"),
    "(select | cell) [inside] (quote | quotes | string)": command(
        "expand-selection-to-quotes:toggle"
    ),
    # needs bracket-matcher atom package; still a bit poor.
    "bracken": command("bracket-matcher:select-inside-bracket"),
    "go match": command("bracket-matcher:go-to-matching-bracket"),
    "remove [matching] (bracket | brackets)": command(
        "bracket-matcher:remove-matching-brackets"
    ),
    "select in quotes": command("expand-selection-quotes"),
    "quinn" + "({})".format(" | ".join(snippets.keys())): code_snippet,
    # '({})'.format(' | '.join(snippets.keys())): code_snippet_naked,
    # python
    "quinn if": ["if :", Key("left")],
    "quinn to do": "# TODO: ",
    # github
    "jet hub open": command("open-on-github:file"),
    "jet hub copy": command("open-on-github:copy-url"),
    "jet hub blame": command("open-on-github:blame"),
    "jet hub repository": command("open-on-github:repository"),
    "jet hub history": command("open-on-github:history"),
    "jet hub issues": command("open-on-github:issues"),
    "jet hub pull requests": command("open-on-github:pull-requests"),
    "jet hub branch compare": command("open-on-github:branch-compare"),
    # autocomplete-python
    "(go to | spring) (definition | def)": command(
        "autocomplete-python:go-to-definition"
    ),
    "show usages": command("autocomplete-python:show-usages"),
    "complete arguments": command("autocomplete-python:complete-arguments"),
    "python rename": command("autocomplete-python:rename"),
    "override method": command("autocomplete-python:override-method"),
    # symbols-view
    "(go to | spring) symbol": command("symbols-view:toggle-file-symbols"),
    "(go to | spring) symbol <dgndictation>": [
        command("symbols-view:toggle-file-symbols"),
        lambda m: time.sleep(0.5),
        text,
        Key("enter"),
        command("center-line:toggle"),
    ],
    # folding
    "fold all": command("editor:fold-all"),
    "unfold all": command("editor:unfold-all"),
    "fold [current row]": command("editor:fold-current-row"),
    "unfold [current row]": command("editor:unfold-current-row"),
    # project
    "add project [folder]": command("application:add-project-folder"),
    "remove project [folder]": command("tree view remove project folder"),
    # blacken
    "blacken": command("atom black blacken"),
    # reflow
    "reflow": Key("cmd-alt-q"),
    "replace [left of] equals [with] return": replace_left_of_equals_with_return,
    # cursor-history
    "(cursor | curr) (previous | preev)": command("cursor history prev"),
    "(cursor | curr) next": command("cursor history next"),
    # config
    "edit snippets": command("application open snippets"),
    "edit key map": command("application open keymap"),
    "install packages": command("settings view install packages and themes"),
}

ctx.keymap(keymap)
