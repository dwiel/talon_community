"""
Since this file is called std, it may be tempting to dump more stuff here.
Ideally, put any new commands in another file, so that related ones are grouped
together, and files don't get massive. This file is currently acting as a
collection of commands that still need to be moved into more appropriate files.
"""

import os

from talon.voice import Word, Context, Key, Rep, RepPhrase, Str, press
from talon import ctrl, clip

ctx = Context("input")

ctx.keymap(
    {
        "trough": Key("alt-backspace"),
        "slap": [Key("cmd-right enter")],
        "sky shock": Key("shift-enter"),
        "ricky": Key("ctrl-e"),
        "lefty": Key("ctrl-a"),
        "olly | ali": Key("cmd-a"),
        "(dot dot | dotdot)": "..",
        "(dot dot dot | dotdotdot)": "...",
        "run (them | vim)": "vim ",
        "dot pie": ".py",
        "word queue": "queue",
        "word eye": "eye",
        "word bson": "bson",
        "word iter": "iter",
        "word cmd": "cmd",
        "word dup": "dup",
        "word (dickt | dictionary)": "dict",
        "word shell": "shell",
        "word talon": "talon",
        "dunder in it": "__init__",
        "string utf8": "'utf8'",
        "shebang bash": "#!/bin/bash -u\n",
        "next tab": Key("cmd-shift-]"),
        "new tab": Key("cmd-t"),
        "(last | prevous | preev) tab": Key("cmd-shift-["),
        "next space": Key("cmd-alt-ctrl-right"),
        "last space": Key("cmd-alt-ctrl-left"),
        "(marco | search)": Key("cmd-f"),
        "marneck": Key("cmd-g"),
        "marpreev": Key("cmd-shift-g"),
        "marthis": [
            Key("alt-right"),
            Key("shift-alt-left"),
            Key("cmd-f"),
            Key("enter"),
        ],
        "(prefies | preferences)": Key("cmd-,"),
        "put computer to sleep": lambda m: os.system("pmset sleepnow"),
    }
)
