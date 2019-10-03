from talon.voice import Context, press

from .. import utils
from ..apps.atom import jump_to_bol
from ..utils import is_filetype, optional_numerals

FILETYPES = (".md",)


def markdown(app, win):
    return is_filetype(FILETYPES)(app, win) or app.bundle == "info.pkpk.inkdrop"


ctx = Context("markdown", func=markdown)


def modify_selected_text(fn):
    def wrapper(m):
        selected = utils.copy_selected("")
        new_lines = []
        for line in selected.split("\n"):
            new_lines.append(fn(m, line))

        utils.paste_text("\n".join(new_lines))

    return wrapper


def modify_line(fn):
    """
    if a number is provided, that line will be modified
    if multiple lines are selected, all lines will be modified
    otherwise, the current line will be modified
    """

    def wrapper(m):
        line_number = utils.extract_num_from_m(m, default=None)
        if line_number is not None:
            jump_to_bol(m)

        selected = utils.copy_selected(None)
        if selected is None:
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
    # righty
    press("cmd-right")
    # lefty
    press("cmd-left")

    # copy this line
    press("cmd-shift-right")
    existing = utils.copy_selected(None)
    if existing is None:
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
