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


def modify_selected_text(fn):
    def wrapper(m):
        utils.paste_text(fn(m, utils.copy_selected("")))

    return wrapper


def modify_line(fn):
    def wrapper(m):
        line_number = utils.extract_num_from_m(m, default=None)
        if line_number is not None:
            jump_to_bol(m)

        # righty
        press("cmd-right")
        # lefty
        press("cmd-left")

        # copy this line
        press("cmd-shift-right")
        modify_selected_text(fn)(m)

    return wrapper


@modify_line
def markdown_complete(m, text):
    return text.replace("- [ ]", "- [X]")


@modify_line
def markdown_incomplete(m, text):
    return text.replace("- [X]", "- [ ]")


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
    utils.snake_text(m)
    press("space")


@modify_line
def markdown_remove_tag(m, text):
    utils.paste_text(
        utils.copy_selected("").replace(" @" + utils.string_capture(m), "")
    )


@modify_line
def markdown_remove_check(m, text):
    return text.replace("[ ] ", "")


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
