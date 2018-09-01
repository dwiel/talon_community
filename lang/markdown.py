from os import system

from talon.voice import Context, Key, press, Str

from ..apps.atom import jump_to_bol
from ..utils import optional_numerals


def markdown_complete(m):
    jump_to_bol(m)
    press("right")
    press("right")
    press("right")
    press("delete")
    Str("X")(None)


def markdown_incomplete(m):
    jump_to_bol(m)
    press("right")
    press("right")
    press("right")
    press("delete")
    Str(" ")(None)


ctx = Context('markdown')

keymap = {
    'markdown check': '- [ ] ',
    'markdown complete' + optional_numerals: markdown_complete,
    'markdown incomplete' + optional_numerals: markdown_incomplete,
}

ctx.keymap(keymap)
