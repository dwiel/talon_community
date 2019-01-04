from talon.voice import Context, Key, Str
from ..misc import basic_keys
from ..utils import parse_words, text
import string

ctx = Context("talon_editor")


def key(m):
    modifiers = basic_keys.get_modifiers(m)
    key = basic_keys.get_keys(m)[0]
    if key is None:
        print("no key", m)
        return
    Str("Key('{}')".format("-".join(modifiers + [key])))(None)


def format_text(fmt):
    def wrapper(m):
        Str(fmt.format(" ".join(parse_words(m))))(None)

    return wrapper


ctx.keymap({
    "key {basic_keys.modifiers}* {basic_keys.keymap}": key,
    "talon map <dgndictation>": ("'", text, "': ,", Key("left")),
    "talon map string <dgndictation>": format_text("'{0}': '{0}',"),
    "dragon dictation": "<dgndictation>",
    "stir": ["Str()(None)"] + [Key("left")] * 7,
})
