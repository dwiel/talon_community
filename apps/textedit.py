import time
from talon.voice import press, Str, Context
from ..utils import numeral_list, extract_num_from_m

ctx = Context("textedit", bundle="com.apple.TextEdit")
ctx.set_list("n", numeral_list)

def select_line(m):
    line_no = extract_num_from_m(m)
    press("cmd-l")
    Str(str(line_no))(None)
    time.sleep(0.1)
    press("enter")


def select_line_and_press(keys=()):
    def fn(m):
        select_line(m)
        for key in keys:
            press(key)

    return fn


ctx.keymap(
    {
        "(select line number | sprinkle) {textedit.n}+": select_line,
        "(go line number {textedit.n}+ start | spring {textedit.n}+)": select_line_and_press(
            ("ctrl-a", "cmd-left")
        ),
        "(go line number {textedit.n}+ end | dear {textedit.n}+)": select_line_and_press(
            ("cmd-right")
        ),
        "(go line number {textedit.n}+ before end | smear {textedit.n}+)": select_line_and_press(
            ("cmd-right", "left")
        ),
        "(new line below number {textedit.n}+ | sprinkoon) {textedit.n}+": select_line_and_press(
            ("cmd-right", "enter")
        ),
        "(delete line number | snipoon ) {textedit.n}+": select_line_and_press(
            ("shift-cmd-right", "delete", "delete", "ctrl-a", "cmd-left")
        ),
    }
)
