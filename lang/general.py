"""
Commands that write bits of code that is valid for multiple languages
"""

from talon.voice import Context, Key

ctx = Context("general_lang")

ctx.keymap(
    {
        # Operators
        # TODO remove duplicates from symbol.py
        "(op equals | assign | equeft)": " = ",
        "(op (minus | subtract) | deminus)": " - ",
        "(op (plus | add) | deplush)": " + ",
        "(op (times | multiply) | duster)": " * ",
        "(op divide | divy)": " / ",
        "op mod": " % ",
        "[op] (minus | subtract) equals": " -= ",
        "[op] (plus | add) equals": " += ",
        "[op] (times | multiply) equals": " *= ",
        "[op] divide equals": " /= ",
        "[op] mod equals": " %= ",
        "(op | is) greater [than]": " > ",
        "(op | is) less [than]": " < ",
        "(op | is) equal": " == ",
        "(op | is) not equal": " != ",
        "(op | is) greater [than] or equal": " >= ",
        "(op | is) less [than] or equal": " <= ",
        "(op (power | exponent) | to the power [of])": " ** ",
        "op and": " && ",
        "op or": " || ",
        "[op] (logical | bitwise) and": " & ",
        "[op] (logical | bitwise) or": " | ",
        "(op | logical | bitwise) (ex | exclusive) or": " ^ ",
        "[(op | logical | bitwise)] (left shift | shift left)": " << ",
        "[(op | logical | bitwise)] (right shift | shift right)": " >> ",
        "(op | logical | bitwise) and equals": " &= ",
        "(op | logical | bitwise) or equals": " |= ",
        "(op | logical | bitwise) (ex | exclusive) or equals": " ^= ",
        "[(op | logical | bitwise)] (left shift | shift left) equals": " <<= ",
        "[(op | logical | bitwise)] (right shift | shift right) equals": " >>= ",
        # Matchables
        # TODO: sort out duplicates from symbol.py
        # TODO: Are these even needed when basically all text editors will
        # automatically enter the closing matchable?
        "args": ["()", Key("left")],
        "index": ["[]", Key("left")],
        "block": [" {}", Key("left enter enter up tab")],
        "empty array": "[]",
        "empty dict": "{}",
        "dickt in it": ["{}", Key("left")],
        "list in it": ["[]", Key("left")],
        "call": "()",
        # Statements
        "state (def | deaf | deft)": "def ",
        "state if": "if ",
        "state else if": [" else if ()", Key("left")],
        "state while": ["while ()", Key("left")],
        "state for": "for ",
        "state switch": ["switch ()", Key("left")],
        "state case": ["case \nbreak;", Key("up")],
        # Other Keywords
        "const": "const ",
        "static": "static ",
        "tip pent": "int ",
        "tip char": "char ",
        "tip byte": "byte ",
        "tip float": "float ",
        "tip double": "double ",
        # Comments
        "comment see": "// ",
        "comment py": "# ",
    }
)
