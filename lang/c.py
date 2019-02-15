from talon.voice import Context, Key

from ..utils import is_filetype

FILETYPES=(".c",)

ctx = Context("c", func=is_filetype(FILETYPES))

ctx.keymap({
    "tip pent 64": "int64_t ",
    "tip you went 64": "uint64_t ",
    "tip pent 32": "int32_t ",
    "tip you went 32": "uint32_t ",
    "tip pent 16": "int16_t ",
    "tip you went 16": "uint16_t ",
    "tip pent 8": "int8_t ",
    "tip you went 8": "uint8_t ",
    "tip size": "size_t",

    "state include": "#include ",
    "state include system": ["#include <>", Key("left")],
    "state include local": ['#include ""', Key("left")],

    "state type deaf": "typedef ",
    "state type deaf struct": ["typedef struct {\n\n};", Key("up"), "\t"],

    "indirect": "&",
    "dereference": "*",

    # Other commands for convenience
    "word streak": ["streq()", Key("left")],
})
