import string
import time
import urllib.parse

from talon import ui
from talon.voice import Context, Key, press
from talon import ctrl
from ...utils import select_single, numerals, delay, paste_text
from ...misc.basic_keys import get_keys
from ...misc import basic_keys
from . import browser

ctx = Context(
    "google_sheets",
    func=lambda app, win: win.title.endswith("- Google Sheets")
    or "- Google Sheets -" in win.title,
)

# def get_url():
#     # TODO: retrieve url in a more direct way
#     press("cmd-l")
#     time.sleep(0.25)
#     copy_selected()


def get_url():
    win = ui.active_window()
    return win.children.find(AXTitle="Address and search bar")[0].AXValue


def set_url(url):
    # update the address bar with the updated URL
    paste_text(url)

    # navigate to new URL
    press("enter")


def update_selected_cell(column, row):
    press("cmd-l")
    url = get_url()
    updated_url = update_query_parameters(url, {"range": "%s%s" % (column, row)})
    set_url(updated_url)


def update_selected_cells(column, row, dest_column, dest_row):
    press("cmd-l")
    url = get_url()
    updated_url = update_query_parameters(
        url, {"range": "%s%s:%s%s" % (column, row, dest_column, dest_row)}
    )
    set_url(updated_url)


def update_query_parameters(url, parameters):
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(parameters)

    url_parts[4] = urllib.parse.urlencode(query)
    url_parts[4] = url_parts[4].replace("%3A", ":")

    # some manual modification because urllib insists on putting the fragment identifier after the query parameters, which is not what we want here
    # fragment = url_parts[5]
    query_string = url_parts[4]
    url_parts[4] = ""  #
    url_parts[5] = url_parts[5].split("?")[0]
    updated_url = urllib.parse.urlunparse(url_parts) + "?" + query_string

    return updated_url


# Talon Sheets command handlers
def go_to_cell(m):
    column = "".join(get_keys(m))
    row = "".join(map(str, m._words[1 + len(column) :]))
    update_selected_cell(column, row)


def go_to_named_cell(m):
    # TODO: how to more easily express intended # of words in command?
    region = str(m._words[1])
    cell = region_map[region]

    update_selected_cell(*cell)


def select_cells(m):
    range = {0: {"column": "", "row": ""}, 1: {"column": "", "row": ""}}

    i = 0
    for word in m._words:
        if word in basic_keys.alphabet.keys():
            if range[i]["row"]:
                i += 1

            range[i]["column"] += basic_keys.alphabet[str(word)]
        elif str(word) in basic_keys.digits:
            range[i]["row"] += str(word)

    update_selected_cells(
        range[0]["column"], range[0]["row"], range[1]["column"], range[1]["row"]
    )


def select_column(m):
    column = "".join(get_keys(m))
    update_selected_cells(column, "", column, "")


def select_row(m):
    row = "".join(map(str, m._words[2:]))
    update_selected_cells("", row, "", row)


## key can only be a single word for now
# TODO: load this from a json file
region_map = {
    # example:
    "home": ("A", "1")
}

alphabet = list(string.ascii_uppercase)
regions = select_single([key for key in region_map.keys() if key not in alphabet])
cycle_offsets = "[" + select_single(list(range(20))[1:]) + "]"
column = "{basic_keys.alphabet}+"
cells = column + numerals

ctx.keymap(
    {
        "rename": [
            Key("alt-/"),
            lambda m: time.sleep(1),
            "rename",
            lambda m: time.sleep(1),
            Key("enter"),
        ],
        # navigation by cell reference
        "(view | go to | spring) " + cells: go_to_cell,
        "edit " + cells: [go_to_cell, delay(1.0), Key("enter")],
        # navigation by name, specified in map above (cell column names, e.g. A-Z, not allowed to avoid conflicting with above cell references)
        # "(view | go to | spring) " + regions: go_to_named_cell,
        "edit " + regions: [go_to_named_cell, delay(1.0), Key("enter")],
        # keyboard shortcut mappings
        "(select range | selrang)" + cells + cells: select_cells,
        "select column": Key("ctrl+space"),
        "select column " + column: select_column,
        "select row": Key("shift+space"),
        "select row " + numerals: select_row,
        "select all": Key("cmd+a"),
        "undo": Key("cmd+z"),
        "redo": Key("cmd+y"),
        # "find": Key("cmd+f"),
        "find and replace": Key("cmd+shift+h"),
        "fill range": Key("cmd+enter"),
        "fill down": Key("cmd+d"),
        "fill right": Key("cmd+r"),
        "save": Key("cmd+s"),
        "open": Key("cmd+o"),
        "print": Key("cmd+p"),
        # "copy": Key("cmd+c"),
        # "cut": Key("cmd+x"),
        # "paste": Key("cmd+v"),
        "(paste values only | paste without formatting)": Key("cmd+shift+v"),
        "(search [the] menus | command pallet)": Key("cmd+/"),
        "compact controls": Key("ctrl+shift+f"),
        "input tools (on | off)": Key("cmd+shift+k"),
        "select input tools": Key("cmd+alt+shift+k"),
        "bold": Key("cmd+b"),
        "underline": Key("cmd+u"),
        "italic": Key("cmd+i"),
        "strikethrough": Key("alt+shift+5"),
        "center align": Key("cmd+shift+e"),
        "left align": Key("cmd+shift+l"),
        "right align": Key("cmd+shift+r"),
        "[apply] (top border | border top)": Key("alt+shift+1"),
        "[apply] (right border | border right)": Key("alt+shift+2"),
        "[apply] (bottom border | border (bottom | below | under))": Key("alt+shift+3"),
        "[apply] (left border | border left)": Key("alt+shift+4"),
        "(remove borders | border remove)": Key("alt+shift+6"),
        "[apply] (outer border | border outer)": Key("alt+shift+7"),
        "insert link": Key("cmd+k"),
        "insert time": Key("cmd+shift+;"),
        "insert date": Key("cmd+;"),
        "insert date and time": Key("cmd+alt+shift+;"),
        "format as (decimal | number)": Key("ctrl+shift+1"),
        "format as time": Key("ctrl+shift+2"),
        "format as date": Key("ctrl+shift+3"),
        "format as currency": Key("ctrl+shift+4"),
        "format as percentage": Key("ctrl+shift+5"),
        "format as exponent": Key("ctrl+shift+6"),
        "clear formatting": Key("cmd+\\"),
        "move to beginning of row": Key("home"),
        "move to beginning of sheet": Key("cmd+home"),
        "move to end of row": Key("end"),
        "move to end of sheet": Key("cmd+end"),
        "sheet move left": [Key("alt-shift-s"), Key("up"), Key("enter")],
        "sheet move right": [Key("alt-shift-s"), Key("up"), Key("up"), Key("enter")],
        "scroll to active cell": Key("cmd+backspace"),
        "(move to next sheet | sheet next)": Key("cmd+shift+pagedown"),
        "(move to previous sheet | sheet previous | sheet prev)": Key(
            "cmd+shift+pageup"
        ),
        "(display list of sheets | sheet list)": Key("alt+shift+k"),
        "sheet new": Key("shift-f11"),
        "sheet rename": [
            Key("alt-shift-s"),
            Key("down"),
            delay(),
            Key("down"),
            delay(),
            Key("down"),
            delay(),
            Key("down"),
            delay(),
            Key("enter"),
        ],
        "sheet duplicate": [
            Key("alt-shift-s"),
            Key("down"),
            delay(),
            Key("down"),
            delay(),
            Key("enter"),
        ],
        "open hyperlink": Key("alt+enter"),
        "open explore": Key("alt+shift+x"),
        "go to side panel": Key("cmd+alt+."),
        "move focus out of spreadsheet": Key("ctrl+cmd+shift+m"),
        "move to quicksum": Key("alt+shift+q"),
        "move focus to popup": lambda m: (
            ctrl.key_press("cmd", ctrl=True, cmd=True, down=True),
            press("e"),
            press("p"),
            ctrl.key_press("cmd", ctrl=True, cmd=True, up=True),
        ),
        "open drop-down menu on filtered cell": Key("ctrl+cmd+r"),
        "open revision history": Key("cmd+alt+shift+h"),
        "open chat inside the spreadsheet": Key("shift+esc"),
        "close drawing editor": Key("cmd+esc"),
        "(insert | edit) note": Key("shift+f2"),
        "(insert | edit) comment": Key("cmd+alt+m"),
        "open comment discussion thread": Key("cmd+alt+shift+a"),
        "enter current comment": lambda m: (
            ctrl.key_press("cmd", ctrl=True, cmd=True, down=True),
            press("e"),
            press("c"),
            ctrl.key_press("cmd", ctrl=True, cmd=True, up=True),
        ),
        "move to next comment": lambda m: (
            ctrl.key_press("cmd", ctrl=True, cmd=True, down=True),
            press("n"),
            press("c"),
            ctrl.key_press("cmd", ctrl=True, cmd=True, up=True),
        ),
        "move to previous comment": lambda m: (
            ctrl.key_press("cmd", ctrl=True, cmd=True, down=True),
            press("p"),
            press("c"),
            ctrl.key_press("cmd", ctrl=True, cmd=True, up=True),
        ),
        "decrease decimal places": [
            Key("alt-/"),
            "decrease decimal places",
            delay(),
            Key("enter"),
        ],
        "increase decimal places": [
            Key("alt-/"),
            "increase decimal places",
            delay(),
            Key("enter"),
        ],
        "file menu": Key("ctrl+alt+f"),
        "edit menu": Key("ctrl+alt+e"),
        "view menu": Key("ctrl+alt+v"),
        "insert menu": Key("ctrl+alt+i"),
        "format menu": Key("ctrl+alt+o"),
        "data menu": Key("ctrl+alt+d"),
        "tools menu": Key("ctrl+alt+t"),
        "open insert menu": Key("cmd+alt+="),
        "open delete menu": Key("cmd+alt+-"),
        "form menu": Key("ctrl+alt+m"),
        "add-ons menu": Key("ctrl+alt+n"),
        "help menu": Key("ctrl+alt+h"),
        "accessibility menu": Key("ctrl+alt+a"),
        "sheet menu": Key("alt+shift+s"),
        "context menu": Key("cmd+shift+\\"),
        "insert (rows | row) above": browser.send_to_page(Key("ctrl+alt+i r")),
        "insert (rows | row) below": browser.send_to_page(Key("ctrl+alt+i b")),
        "insert (columns | column) [to the] left": browser.send_to_page(
            Key("ctrl-alt-i c")
        ),
        "insert (columns | column) [to the] right": browser.send_to_page(
            Key("ctrl+alt+i o")
        ),
        "delete (rows | row)": browser.send_to_page(Key("ctrl+alt+e d")),
        "delete (columns | column)": Key("cmd+alt+-"),
        "hide row": Key("cmd+alt+9"),
        "hide column": Key("cmd+alt+0"),
        "group (rows | row) or (columns | column)": Key("alt+shift+right"),
        "ungroup (rows | row) or (columns | column)": Key("alt+shift+left"),
        "expand grouped (rows | row) or (columns | column)": Key("alt+shift+down"),
        "collapse grouped (rows | row) or (columns | column)": Key("alt+shift+up"),
        "show all formulas": Key("ctrl+~"),
        "insert array formula": Key("cmd+shift+enter"),
        "collapse an expanded array formula": Key("cmd+e"),
        "(show | hide) formula help": Key("shift+f1"),
        "(full | compact) formula help": Key("f1"),
        "(absolute | relative) references": Key("f4"),
        "toggle formula result previews": Key("f9"),
        "resize formula bar up": Key("ctrl+alt+up"),
        "resize formula bar down": Key("ctrl+option+down"),
        "turn on screen reader support": Key("cmd+alt+z"),
        "read column": Key("cmd+alt+shift+c"),
        "read row": Key("cmd+alt+shift+r"),
        "(resize column | column resize)": [
            Key("up"),
            Key("down"),
            Key("ctrl+space"),
            Key("ctrl+space"),
            Key("cmd+shift+\\"),
            delay(),
        ]
        + [Key("down")] * 9
        + [Key("enter")],
    }
)
