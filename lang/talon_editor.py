import string

from talon.voice import Context, Key, Str, press
from talon import clip

from ..apps import atom
from ..misc import basic_keys
from ..misc import switcher
from ..utils import parse_words, text, is_filetype, paste_text, insert

FILETYPES = (".py",)

ctx = Context("talon_editor", func=is_filetype(FILETYPES))


def make_key(function_name="Key"):
    def key(m):
        modifiers = basic_keys.get_modifiers(m)
        key = basic_keys.get_keys(m)[0]
        if key is None:
            print("no key", m)
            return
        key_text = "-".join(modifiers + [key])
        Str(f'{function_name}("{key_text}")')(None)

    return key


def format_text(fmt):
    def wrapper(m):
        Str(fmt.format(" ".join(parse_words(m))))(None)

    return wrapper


def add_alternative(m):
    try:
        with clip.capture() as s:
            press("cmd-c")
        existing = s.get()
    except clip.NoChange:
        return

    paste_text(f"({existing} | )")
    press("left")
    text(m)


def dragon_abbreviation(m):
    keys = basic_keys.get_keys(m)
    insert(" ".join(key.upper() for key in keys))


def edit_context(m):
    press("ctrl-9")
    switcher.switch_app("Atom")
    atom.open_fuzzy_file(m)


ctx.keymap(
    {
        "key {basic_keys.modifiers}* {basic_keys.keymap}": make_key("Key"),
        "press {basic_keys.modifiers}* {basic_keys.keymap}": make_key("press"),
        "talon map <dgndictation>": ("'", text, "': ,", Key("left")),
        "talon map string <dgndictation>": format_text("'{0}': '{0}',"),
        "dragon dictation": "<dgndictation>",
        "stir": ["Str()(None)"] + [Key("left")] * 7,
        "add alternative [<dgndictation>]": add_alternative,
        "dragon abbreviation {basic_keys.keymap}+": dragon_abbreviation,
    }
)

global_ctx = Context("talon_editor_global")
global_ctx.keymap({"edit context <dgndictation>": edit_context})
