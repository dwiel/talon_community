import time
from talon.voice import press, Str, Context
from ..utils import extract_num_from_m

ctx = Context("textedit", bundle="com.apple.TextEdit")


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
        "(select line number | sprinkle) {n.all}+": select_line,
        "(go line number {n.all}+ start | spring {n.all}+)": select_line_and_press(
            ("ctrl-a", "cmd-left")
        ),
        "(go line number {n.all}+ end | dear {n.all}+)": select_line_and_press(
            ("cmd-right")
        ),
        "(go line number {n.all}+ before end | smear {n.all}+)": select_line_and_press(
            ("cmd-right", "left")
        ),
        "(new line below number {n.all}+ | sprinkoon) {n.all}+": select_line_and_press(
            ("cmd-right", "enter")
        ),
        "(delete line number | snipoon ) {n.all}+": select_line_and_press(
            ("shift-cmd-right", "delete", "delete", "ctrl-a", "cmd-left")
        ),
    }
)
