"""
Commands that write bits of code that is valid for multiple languages
"""

from talon.voice import Context, Key

ctx = Context("general_lang")

ctx.keymap(
    {
        # Operators
        "(op equals | assign | equeft)": " = ",
        "(op (minus | subtract) | deminus)": " - ",
        "(op (plus | add) | deplush)": " + ",
        "(op (times | multiply) | duster)": " * ",
        "(op divide | divy)": " / ",
        "op mod": " % ",
        "((op minus | subtract) equals | minus assign)": " -= ",
        "((op plus | add) equals | (plus | add) assign)": " += ",
        "([op] (times | multiply) (assign | equals) | star assign)": " *= ",
        "[op] divide (assign | equals)": " /= ",
        "[op] mod (assign | equals)": " %= ",
        "(op colon (equals | assign) | coleek)": " := ",
        "(op | is) greater [than]": " > ",
        "(op | is) less [than]": " < ",
        "((op | is) equal [to] | longqual)": " == ",
        "((op | is) not equal [to] | banquall)": " != ",
        "((op | is) greater [than] or equal [to] | grayqual)": " >= ",
        "((op | is) less [than] or equal [to] | lessqual)": " <= ",
        "([(op | is)] exactly (equal [to] | equals) | triple equals | trickle)": " === ",
        "([(op | is)] not exactly (equal [to] | equals) | ranqual | nockle)": " !== ",
        "(op (power | exponent) | to the power [of])": " ** ",
        "op and": " && ",
        "op or": " || ",
        "[op] (logical | bitwise) and": " & ",
        "([op] (logical | bitwise) or | (op | D) pipe)": " | ",
        "[(op | logical | bitwise)] (ex | exclusive) or": " ^ ",
        "(op | logical | bitwise) (left shift | shift left)": " << ",
        "(op | logical | bitwise) (right shift | shift right)": " >> ",
        "(op | logical | bitwise) and equals": " &= ",
        "(op | logical | bitwise) or equals": " |= ",
        "(op | logical | bitwise) (ex | exclusive) or equals": " ^= ",
        "[(op | logical | bitwise)] (left shift | shift left) equals": " <<= ",
        "[(op | logical | bitwise)] (right shift | shift right) equals": " >>= ",
        "[op] (arrow | lambo)": " -> ",
        "[op] fat (arrow | lambo)": " => ",
        # Inside matchables
        "(list in it | index | brax)": ["[]", Key("left")],
        "angler": ["<>", Key("left")],
        "coif": ['""', Key("left")],
        "glitch": ["``", Key("left")],
        "(dickt in it | kirk)": ["{}", Key("left")],
        "precoif": ['("")', Key("left"), Key("left")],
        "(prex | args)": ["()", Key("left")],
        "posh": ["''", Key("left")],
        "dunder": ["____", Key("left left")],
        # Completed matchables
        "(empty parens | call)": "()",
        "empty (dict | object)": "{}",
        "(empty array | brackers)": "[]",
        # Blocks
        "[brace] block": [" {}", Key("left enter enter up tab")],
        "(square | brax) | block": ["[", Key("enter")],
        "(paren | prex) block": ["(", Key("enter")],
        # Combos
        "coalshock": [":", Key("enter")],
        "comshock": [",", Key("enter")],
        "sinker": [Key("cmd-right ;")],
        "swipe": ", ",
        "coalgap": ": ",
        "[forward] slasher": "// ",
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
