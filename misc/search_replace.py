from talon.voice import Context, Key, press
from .. import utils

ctx = Context("search_replace")


def marthis(m):
    selected = utils.copy_selected()
    if selected:
        press("cmd-f")
        utils.paste_text(selected)
        press("enter")
    else:
        press("alt-right")
        press("shift-alt-left")
        press("cmd-f")
        press("enter")


keymap = {
    "marco [<dgndictation>] [over]": [Key("cmd-f"), utils.text, Key("enter")],
    "marneck": Key("cmd-g"),
    "marpreev": Key("cmd-shift-g"),
    "marthis": marthis,
    "(find selected text | find selection | sell find)": Key("cmd-e cmd-f enter"),
    "set selection [text]": Key("cmd-e"),
    "set replacement [text]": Key("cmd-shift-e"),
    "([ (search | find) ] [and] replace (selected text | selection) | sell find ace)": Key(
        "cmd-e cmd-alt-f"
    ),
    "([ (search | find) ] [and] replace [text] | find ace)": Key("cmd-alt-f"),
}

ctx.keymap(keymap)
