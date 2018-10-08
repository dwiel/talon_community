from talon.voice import Context, Key, Str
from ..misc import std
from ..utils import parse_words, text
import string

ctx = Context("talon_editor")


def key(m):
    words = [str(word).lower() for word in m._words]
    modifiers = []
    if "command" in words:
        modifiers.append("cmd")
    if "shift" in words:
        modifiers.append("shift")
    if "control" in words:
        modifiers.append("ctrl")
    if "option" in words or "alt" in words:
        modifiers.append("alt")

    key = None
    for word in words:
        if word in alnum:
            key = alnum[word]
        if word in string.ascii_lowercase:
            key = word

    if key is None:
        print("no key", words)
        return

    Str("Key('{}')".format("-".join(modifiers + [key])))(None)


def format_text(fmt):
    def wrapper(m):
        Str(fmt.format(" ".join(parse_words(m))))(None)

    return wrapper


alnum = dict(std.keys)

keys = "({})".format(" | ".join(list(alnum.keys()) + list(string.ascii_uppercase)))

ctx.keymap(
    {
        "key (command | shift | control | alt | option)* " + keys: key,
        "map <dgndictation>": ("'", text, "': ,", Key("left")),
        "map string <dgndictation>": format_text("'{0}': '{0}',"),
        "dragon dictation": "<dgndictation>",
        "stir": ["Str()(None)"] + [Key("left")] * 7,
    }
)
