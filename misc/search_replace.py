from talon.voice import Context, Key
from ..utils import text

ctx = Context("search_replace")

keymap = {
    "(find | search | marco) [<dgndictation>] [over]": [Key("cmd-f"), text, Key("enter")],
    "marneck": Key("cmd-g"),
    "marpreev": Key("cmd-shift-g"),
    "marthis": [Key("alt-right"), Key("shift-alt-left"), Key("cmd-f"), Key("enter")],
    "(find selected text | find selection | sell find)": Key("cmd-e cmd-f enter"),
    "set selection [text]": Key("cmd-e"),
    "set replacement [text]": Key("cmd-shift-e"),
    "([ (search | find) ] [and] replace (selected text | selection) | sell find ace)": Key(
        "cmd-e cmd-alt-f"
    ),
    "([ (search | find) ] [and] replace [text] | find ace)": Key("cmd-alt-f"),
}

ctx.keymap(keymap)
