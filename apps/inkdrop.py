from talon.voice import Context, Key, Rule, press

from .. import utils

ctx = Context("inkdrop", bundle="info.pkpk.inkdrop")


def go_to_line(m):
    if isinstance(m, Rule):
        line = utils.extract_num_from_m(m, default=None)
    else:
        line = m

    press("ctrl-g")
    utils.paste_text(line)
    press("enter")


ctx.keymap(
    {
        "spring" + utils.numerals: go_to_line,
        "goneck": Key("cmd-shift-]"),
        "goprev": Key("cmd-shift-["),
    }
)
