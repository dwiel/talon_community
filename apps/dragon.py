from talon.api import ffi
from talon.voice import Context, Key
from talon import ctrl, applescript
import time


def open_dragon_pad(m):
    old = ctrl.mouse_pos()
    x = applescript.run(
        """
    tell application "System Events" to tell process "Dragon" to tell (menu bar item 1 of menu bar 2)
        set AppleScript's text item delimiters to ", "
        position as string
    end tell
    """
    )
    x, y = map(int, x.split(", "))
    ctrl.mouse(x, y)
    ctrl.mouse_click()
    ctrl.mouse(*old)
    applescript.run(
        """
    tell application "System Events" to tell process "Dragon" to tell (menu bar item 1 of menu bar 2)
        click menu item "Help" of menu 1
        click menu item "DragonPad" of menu of menu item "Help" of menu 1
    end tell
    """
    )


ctx = Context("dragon")
ctx.keymap({"dragonpad": open_dragon_pad})
