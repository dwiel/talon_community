"""
"""

import os

from talon.voice import Context, Key

ctx = Context("tabs")

ctx.keymap(
    {
        "new tab": Key("cmd-t"),
        "next tab": Key("cmd-shift-]"),
        "(last | prevous | preev) tab": Key("cmd-shift-["),
    }
)
