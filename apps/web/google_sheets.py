import string
import urllib.parse
import time

from talon.voice import Context, Key, Str, press
from talon import ctrl, clip

from ..utils import select_single, numerals, delay
from ..misc.basic_keys import get_keys

ctx = Context(
    "google_sheets",
    func=lambda app, win: win.title.endswith("- Google Sheets")
    or "- Google Sheets -" in win.title,
)


def get_url():
    # TODO: retrieve url in a more direct way
    press("cmd-l")
    time.sleep(0.25)
    press("cmd-c")
    time.sleep(0.25)
    return clip.get()


def update_range(column, row):
    url = get_url()
    print(("url", url))

    # TODO: handle malformed URL (including the case where there is gibberish in the address bar)
    updated_url = update_query_parameters(url, {"range": r"%s%s" % (column, row)})
    print(("updated_url", updated_url))

    # update the address bar with the updated URL
    clip.set(updated_url)
    time.sleep(0.25)
    press("cmd-v")

    # navigate to new URL
    press("enter")


def update_query_parameters(url, parameters):
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(parameters)

    url_parts[4] = urllib.parse.urlencode(query)

    # some manual modification because urllib insists on putting the fragment identifier after the query parameters, which is not what we want here
    fragment = url_parts[5]
    query_string = url_parts[4]
    url_parts[4] = ""  #
    url_parts[5] = url_parts[5].split("?")[0]
    updated_url = urllib.parse.urlunparse(url_parts) + "?" + query_string

    return updated_url


# Talon Sheets command handlers
def go_to_cell():
    def _go_to_cell(m):
        # TODO: support columns with multiple characters: AC
        column = "".join(get_keys(m))
        row = str(m._words[2])
        update_range(column, row)

    return _go_to_cell


def go_to_named_cell():
    def _go_to_named_cell(m):
        # TODO: how to more easily express intended # of words in command?
        region = str(m._words[1])
        cell = region_map[region]

        update_range(*cell)

    return _go_to_named_cell


## key can only be a single word for now
# TODO: load this from a json file
region_map = {
    # example:
    "home": ("A", "1")
}

alphabet = list(string.ascii_uppercase)
regions = select_single([key for key in region_map.keys() if key not in alphabet])
cycle_offsets = "[" + select_single(list(range(20))[1:]) + "]"
cells = "{basic_keys.alphabet}+" + numerals

ctx.keymap(
    {
        # navigation by cell reference
        "(view | go to | spring) " + cells: go_to_cell(),
        "edit " + cells: [go_to_cell(), delay(1.0), Key("enter")],
        # navigation by name, specified in map above (cell column names, e.g. A-Z, not allowed to avoid conflicting with above cell references)
        "(view | go to | spring) " + regions: go_to_named_cell(),
        "edit " + regions: [go_to_named_cell(), delay(1.0), Key("enter")],
        # keyboard shortcut mappings
        "select column": Key("ctrl+space"),
        "select row": Key("shift+space"),
        "select all": Key("cmd+a"),
        "undo": Key("cmd+z"),
        "redo": Key("cmd+y"),
        "find": Key("cmd+f"),
        "find and replace": Key("cmd+shift+h"),
        "fill range": Key("cmd+enter"),
        "fill down": Key("cmd+d"),
        "fill right": Key("cmd+r"),
        "save": Key("cmd+s"),
        "open": Key("cmd+o"),
        "print": Key("cmd+p"),
        "copy": Key("cmd+c"),
        "cut": Key("cmd+x"),
        "paste": Key("cmd+v"),
        "paste values only": Key("cmd+shift+v"),
        "show common keyboard shortcuts": Key("cmd+/"),
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
        "apply (top border | border top)": Key("alt+shift+1"),
        "apply (right border | border right)": Key("alt+shift+2"),
        "apply (bottom border | border bottom)": Key("alt+shift+3"),
        "apply (left border | border left)": Key("alt+shift+4"),
        "remove borders": Key("alt+shift+6"),
        "apply outer border": Key("alt+shift+7"),
        "insert link": Key("cmd+k"),
        "insert time": Key("cmd+shift+;"),
        "insert date": Key("cmd+;"),
        "insert date and time": Key("cmd+alt+shift+;"),
        "format as decimal": Key("ctrl+shift+1"),
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
        "scroll to active cell": Key("cmd+backspace"),
        "move to next sheet": Key("cmd+shift+pagedown"),
        "move to previous sheet": Key("cmd+shift+pageup"),
        "display list of sheets": Key("alt+shift+k"),
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
        "insert (rows | row) above": Key("ctrl+alt+i r"),
        "insert (rows | row) below": Key("ctrl+alt+i b"),
        "insert (columns | column) to the left": Key("ctrl-alt-i c"),
        "insert (columns | column) to the right": Key("ctrl+alt+i o"),
        "delete (rows | row)": Key("ctrl+alt+e d"),
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
    }
)
