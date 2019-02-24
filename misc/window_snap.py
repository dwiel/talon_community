from talon import ui, tap
from talon.voice import Context

"""Provides a voice-driven window management application implemented in Talon.

You can use this to replace applications like Spectacle, BetterSnapTool, and Divvy.

Todo:
    - Provide for mapping keyboard shortcuts as a fallback when the new API is launched.
"""


def move_screen(off):
    win = ui.active_window()
    src_screen = win.screen
    screens = ui.screens()
    dst_screen = screens[(screens.index(src_screen) + off) % len(screens)]
    if src_screen == dst_screen:
        return

    src = src_screen.visible_rect
    dst = dst_screen.visible_rect
    old = win.rect
    win.rect = ui.Rect(
        dst.left + (old.left - src.left) / src.width * dst.width,
        dst.top + (old.top - src.top) / src.height * dst.height,
        old.width / src.width * dst.width,
        old.height / src.height * dst.height,
    )


def resize_window(x, y, w, h):
    print("Resizing: ", x, y, w, h)
    win = ui.active_window()
    rect = win.screen.visible_rect.copy()
    rect.x += rect.width * x
    rect.y += rect.height * y
    rect.width *= w
    rect.height *= h
    win.rect = rect


def resize_to_grid(column, row, columns, rows, colspan=1, rowspan=1):
    # Ensure sane values for column and row (> 1, <= columns/rows)
    column = max(min(column, columns), 1)
    row = max(min(row, rows), 1)

    # Ensure sane values for column/row spans (e.g. if there are 3 columns, column 3 with rowspan 2 or column 2 with
    # rowspan 3 doesn't make sense). One can only span as many columns as are remaining to the right/rows downward.
    columns_remaining = columns - column
    colspan = min(max(colspan, 1), columns_remaining + 1)
    rows_remaining = rows - row
    rowspan = min(max(rowspan, 1), rows_remaining + 1)

    # Convert the grid pattern passed to the function into position and size information, then pass to resize_window().
    # We subtract 1 column/row because we need the starting position of the column, which is the ending position of the
    # previous one.
    x = (column / columns) - (1 / columns)
    y = (row / rows) - (1 / rows)

    # Width and height are just percentages. The resize function converts them to actual width/height.
    w = (1 / columns) * colspan
    h = (1 / rows) * rowspan

    resize_window(x, y, w, h)


def grid(column, row, columns, rows, colspan=1, rowspan=1):
    """Resize and move a window to a specific column and row within a grid of columns and rows. Optionally, you can
    span multiple rows or columns (to achieve things like "right two-thirds").

    Examples:
        1, 1, 2, 2: moves to top-left fourth (corner) of screen
        3, 1, 3, 1: moves to right third of screen
        3, 2, 3, 3: on a 3x3 grid, moves to the second row (out of three) on the rightmost third of the screen. In other
        words, it forms a box as tall as one-third of the screen (as that is the height of a row).
        2, 1, 3, 1, 2: right two-thirds, full height (starting at column 2 of 3, spanning two columns)
    """
    return lambda m: resize_to_grid(column, row, columns, rows, colspan, rowspan)


def next_screen(m):
    move_screen(1)


def previous_screen(m):
    move_screen(-1)


ctx = Context('window_snap')
ctx.keymap({
    'snap left':         grid(1, 1, 2, 1),
    'snap right':        grid(2, 1, 2, 1),
    'snap top':          grid(1, 1, 1, 2),
    'snap bottom':       grid(1, 2, 1, 2),
    'snap top left':     grid(1, 1, 2, 2),
    'snap top right':    grid(2, 1, 2, 2),
    'snap bottom left':  grid(1, 2, 2, 2),
    'snap bottom right': grid(2, 2, 2, 2),
    'snap screen':       grid(1, 1, 1, 1),
    'snap next':         next_screen,
    'snap last':         previous_screen,
})
