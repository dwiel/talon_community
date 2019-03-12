from talon.voice import Context, Key

from ..utils import is_filetype, snake_text

FILETYPES = (".py",)

ctx = Context("python", func=is_filetype(FILETYPES))
# ctx = Context("python")

ctx.keymap(
    {
        "state any": ["any()", Key("left")],
        "dunder in it": "__init__",
        "dot pie": ".py",
        "dot pipe": ".py",
        "self assign <dgndictation> [over]": [
            "self.",
            snake_text,
            " = ",
            snake_text,
            "\n",
        ],
        "star arguments": "*args",
        "star star K wargs": "**kwargs",
    }
)

# TODO: defined function
# TODO: defined class
# TODO: python-ast
# TODO: don't overload tab for quinn snippet navigation
