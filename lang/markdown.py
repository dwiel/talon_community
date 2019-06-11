from os import system

from talon.voice import Context, Key, press, Str
from talon import clip

from ..apps.atom import jump_to_bol
from ..utils import optional_numerals, is_filetype, text
from .. import utils


FILETYPES = (".md",)


def markdown(app, win):
    return is_filetype(FILETYPES)(app, win) or app.bundle == "info.pkpk.inkdrop"


ctx = Context("markdown", func=markdown)


def markdown_complete(m):
    if len(m._words) > 2:
        jump_to_bol(m)
    else:
        # righty
        press("cmd-right")
        # lefty
        press("cmd-left")

    press("right")
    press("right")
    press("right")
    press("delete")
    Str("X")(None)


def markdown_incomplete(m):
    if len(m._words) > 2:
        jump_to_bol(m)
    else:
        # righty
        press("cmd-right")
        # lefty
        press("cmd-left")

    press("right")
    press("right")
    press("right")
    press("delete")
    Str(" ")(None)


def markdown_add_tag(m):
    # if len(m._words) > 2:
    #     jump_to_bol(m)
    # else:

    # righty
    press("cmd-right")
    # lefty
    press("cmd-left")

    # copy this line
    press("cmd-shift-right")
    try:
        with clip.capture() as s:
            press("cmd-c")
        existing = s.get()
    except clip.NoChange:
        return
    press("left")

    print(existing)
    if existing[:5] == "- [ ]" or existing[:5] == "- [X]":
        press("right")
        press("right")
        press("right")
        press("right")
        press("right")
        press("right")

    press("@")
    text(m)
    press("space")


def markdown_remove_tag(m):
    # righty
    press("cmd-right")
    # lefty
    press("cmd-left")

    # copy this line
    press("cmd-shift-right")
    try:
        with clip.capture() as s:
            press("cmd-c")
        existing = s.get()
    except clip.NoChange:
        return

    utils.paste_text(existing.replace(" @" + utils.string_capture(m), ""))


def markdown_remove_check(m):
    line_number = utils.extract_num_from_m(m, default=None)
    if line_number is not None:
        jump_to_bol(m)

    # righty
    press("cmd-right")
    # lefty
    press("cmd-left")

    # copy this line
    press("cmd-shift-right")
    utils.paste_text(utils.copy_selected("").replace("[ ] ", ""))


keymap = {
    "markdown check": "- [ ] ",
    "[markdown] remove check" + optional_numerals: markdown_remove_check,
    "markdown complete" + optional_numerals: markdown_complete,
    "markdown incomplete" + optional_numerals: markdown_incomplete,
    # "add tag " + optional_numeral + "<dgndictation>": markdown_add_tag,
    "[add] tag <dgndictation>": markdown_add_tag,
    "remove tag <dgndictation>": markdown_remove_tag,
}

ctx.keymap(keymap)
