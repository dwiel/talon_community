import os
import json
import time
import contextlib

from talon import ui, resource, ctrl
from talon.voice import Key, Context, press

from .. import utils


single_digits = "0123456789"
NAMED_DESKTOPS = {digit: int(digit) for digit in single_digits}
desktops_filename = utils.local_filename(__file__, "named_desktops.json")
NAMED_DESKTOPS.update(json.load(resource.open(desktops_filename)))


@contextlib.contextmanager
def drag_window(win=None):
    if win is None:
        win = ui.active_window()
    fs = win.children.find(AXSubrole="AXFullScreenButton")[0]
    rect = fs.AXFrame["$rect2d"]
    x = rect["x"] + rect["width"] + 5
    y = rect["y"] + rect["height"] / 2
    ctrl.mouse_move(x, y)
    ctrl.mouse_click(button=0, down=True)
    yield
    time.sleep(0.1)
    ctrl.mouse_click(button=0, up=True)


def move_win_left_space(m):
    with drag_window():
        press("ctrl-cmd-alt-left")


def move_win_right_space(m):
    with drag_window():
        press("ctrl-cmd-alt-right")


def window_move_space(m):
    desktop_number = NAMED_DESKTOPS[m["spaces.named_desktops"][0]]
    with drag_window():
        press(f"ctrl-{desktop_number}")


keymap = {"window move (space | desk) {spaces.named_desktops}": window_move_space}
keymap.update(
    {
        "(space | desk) %s" % name: Key("ctrl-%s" % NAMED_DESKTOPS[name])
        for name in NAMED_DESKTOPS.keys()
    }
)

ctx = Context("spaces")
ctx.keymap(keymap)
ctx.set_list("named_desktops", NAMED_DESKTOPS.keys())
