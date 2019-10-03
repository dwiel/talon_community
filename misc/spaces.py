import contextlib
import json
import time

from talon import cron, ctrl, resource, ui
from talon.voice import Context, press

from .. import utils
from . import last_phrase

single_digits = "0123456789"
NAMED_DESKTOPS = {digit: int(digit) for digit in single_digits}
desktops_filename = utils.local_filename(__file__, "named_desktops.json")
NAMED_DESKTOPS.update(json.load(resource.open(desktops_filename)))


def amethyst_running():
    return bool(ui.apps(bundle="com.amethyst.Amethyst"))


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
    if amethyst_running():
        press(f"ctrl-alt-shift-{desktop_number}")
    else:
        with drag_window():
            press(f"ctrl-{desktop_number}")


def desk(m=None, desktop_number=None):
    if m:
        desktop_number = NAMED_DESKTOPS[m["spaces.named_desktops"][0]]

    press(f"ctrl-{desktop_number}")
    cron.after("300ms", last_phrase.history.refresh)


keymap = {
    "window move (space | desk) {spaces.named_desktops}": window_move_space,
    "desk {spaces.named_desktops}": desk,
}

ctx = Context("spaces")
ctx.keymap(keymap)
ctx.set_list("named_desktops", NAMED_DESKTOPS.keys())
