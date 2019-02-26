from talon.voice import Context, Key, press
import talon.clip as clip
from ..utils import (
    text,
    parse_words,
    parse_words_as_integer,
    insert,
    word,
    join_words,
    is_filetype,
)

JS_EXTENSIONS = (".js", ".jsx")

context = Context("javascript", func=is_filetype(JS_EXTENSIONS))


def remove_spaces_around_dashes(m):
    words = parse_words(m)
    s = " ".join(words)
    s = s.replace(" – ", "-")
    insert(s)


def CursorText(s):
    left, right = s.split("{.}", 1)
    return [left + right, Key(" ".join(["left"] * len(right)))]


context.keymap(
    {
        "const [<dgndictation>]": ["const ", text],
        "let [<dgndictation>]": ["let ", text],
        "static": "static ",
        "args": ["()", Key("left")],
        "index": ["[]", Key("left")],
        "block": [" {}", Key("left enter enter up tab")],
        "empty array": "[]",
        "empty object": "{}",
        "call": "()",
        "state func": "function ",
        "state return": "return ",
        "state constructor": "constructor ",
        "state if": ["if ()", Key("left")],
        "state else": " else ",
        "state else if": [" else if ()", Key("left")],
        "state while": ["while ()", Key("left")],
        "state for": ["for ()", Key("left")],
        "state switch": ["switch ()", Key("left")],
        "state case": ["case \nbreak;", Key("up")],
        "state goto": "goto ",
        "state important": "import ",
        "state class": "class ",
        "state extends": "extends ",
        "state super": "super",
        "comment js": "// ",
        "word no": "null",
        "arrow": " => ",
        "assign": " = ",
        "asink": " async ",
        "op (minus | subtract)": " - ",
        "op (plus | add)": " + ",
        "op (times | multiply)": " * ",
        "op divide": " / ",
        "op mod": " % ",
        "[op] (minus | subtract) equals": " -= ",
        "[op] (plus | add) equals": " += ",
        "[op] (times | multiply) equals": " *= ",
        "[op] divide equals": " /= ",
        "[op] mod equals": " %= ",
        "(op | is) greater [than]": " > ",
        "(op | is) less [than]": " < ",
        "(op | is) equal": " === ",
        "(op | is) not equal": " !== ",
        "(op | is) greater [than] or equal": " >= ",
        "(op | is) less [than] or equal": " <= ",
        "(op (power | exponent) | to the power [of])": " ** ",
        "op and": " && ",
        "op or": " || ",
        # utility snippets
        "log": "log",
        "log error": "logE",
        "log object": "logD",
        "axe": "ImportAxios",
        "require": "requireMOD",
        # commands for express
        "express import": "ImportExpress",
        "express initialize": "InitializeApplication",
        "expressive initialize": "InitializeRouter",
        "expressive use": "ExpressRouterUse",
        "express use": "ExpressApplicationUse",
        "express callback": "ExpressRouteCb",
        "expressive route": "RouterRoute",
        "express route": "ApplicationRoute",
        # commands for sequelize
        "model import": "ImportDB",
        "model initialize": "DBInit",
        "model equalize": "Sequelize",
        "model nag": "allowNull",
        # commands for react
        "react import": "ImportReact",
        "react tag": ["< />", Key("left left left")],
        "react clack": "onClick",
        # need to add snippets for components
        "react component": ["React.Component ", Key("left")],
        # commands for react dom
        "document import": "ImportDOM",
        "document import hash": "ImportHash",
        "document import browser": "ImportBrowser",
        "document render": ["ReactDOM.render()", Key("left")],
        # commands for redux
        "store import": "ImportRedux",
        "store logger": "ImportLogger",
        "store think": "ImportThunk",
        "store combine": "ImportReducers",
        "store create": "MakeStore",
        # commands for react-redux
        "combo provider": "ImportProvider",
    }
)
