import re

from talon.voice import Context, Key, press

from ..utils import is_filetype, snake_text, insert
from .. import utils

FILETYPES = (".py",)

ctx = Context("global_python")
exception_list = [
    "BaseException",
    "SystemExit",
    "KeyboardInterrupt",
    "GeneratorExit",
    "Exception",
    "StopIteration",
    "StopAsyncIteration",
    "ArithmeticError",
    "FloatingPointError",
    "OverflowError",
    "ZeroDivisionError",
    "AssertionError",
    "AttributeError",
    "BufferError",
    "EOFError",
    "ImportError",
    "ModuleNotFoundError",
    "LookupError",
    "IndexError",
    "KeyError",
    "MemoryError",
    "NameError",
    "UnboundLocalError",
    "OSError",
    "BlockingIOError",
    "ChildProcessError",
    "ConnectionError",
    "BrokenPipeError",
    "ConnectionAbortedError",
    "ConnectionRefusedError",
    "ConnectionResetError",
    "FileExistsError",
    "FileNotFoundError",
    "InterruptedError",
    "IsADirectoryError",
    "NotADirectoryError",
    "PermissionError",
    "ProcessLookupError",
    "TimeoutError",
    "ReferenceError",
    "RuntimeError",
    "NotImplementedError",
    "RecursionError",
    "SyntaxError",
    "IndentationError",
    "TabError",
    "SystemError",
    "TypeError",
    "ValueError",
    "UnicodeError",
    "UnicodeDecodeError",
    "UnicodeEncodeError",
    "UnicodeTranslateError",
    "Warning",
    "DeprecationWarning",
    "PendingDeprecationWarning",
    "RuntimeWarning",
    "SyntaxWarning",
    "UserWarning",
    "FutureWarning",
    "ImportWarning",
    "UnicodeWarning",
    "BytesWarning",
    "ResourceWarning",
]
exceptions = {
    " ".join(re.findall("[A-Z][^A-Z]*", exception)): exception
    for exception in exception_list
}


def raise_exception(m):
    insert(f"raise {exceptions[m['global_python.exception'][0]]}()")
    press("left")


def modify_selected_text(fn):
    def wrapper(m):
        utils.paste_text(fn(m, utils.copy_selected("")))

    return wrapper


def wrap_call(m):
    text = f"({utils.copy_selected('')})"
    utils.paste_text(text)
    for _ in range(len(text)):
        press("left")

    utils.snake_text(m)


ctx.keymap(
    {
        "dunder in it": "__init__",
        "dot pie": ".py",
        "dot pipe": ".py",
        "star (arguments | args)": "*args",
        "star star K wargs": "**kwargs",
        "raise value error": ["raise ValueError()", Key("left")],
        "raise not implemented error": "raise NotImplementedError()",
        "raise {global_python.exception}": raise_exception,
    }
)
ctx.set_list("exception", exceptions.keys())

ctx = Context("python", func=is_filetype(FILETYPES))
ctx.keymap(
    {
        "self assign <dgndictation> [over]": [
            "self.",
            snake_text,
            " = ",
            snake_text,
            "\n",
        ],
        "self": "self",
        "self dot": "self.",
        "self [(dot | doubt)] <dgndictation> [over]": ["self.", snake_text],
        "self [(dot | doubt)] private <dgndictation> [over]": ["self._", snake_text],
        "import [<dgndictation>] [over]": ["import ", snake_text],
        "from [<dgndictation>] [over]": ["from ", snake_text],
        # this isn't easy to write because snake_text always assumes it is
        # working on # the first <dgndictation>, but this command has two of
        # them
        # "from <dgndictation> import [<dgndictation>] [over]": from_import ,
        "in": " in ",
        "is": " is ",
        "is not": " is not ",
        "true": "True",
        "champ true": "True",
        "false": "False",
        "champ false": "False",
        "none": "None",
        "champ none": "None",
        "F string": [lambda m: utils.paste_text("f'{}'"), Key("left"), Key("left")],
        "wrap call [<dgndictation>]": wrap_call,
        # "if": ["if :", Key("left")],
        "else": "else:\n",
        "with": ["with :", Key("left")],
        "return [<dgndictation>] [over]": ["return ", snake_text],
        "set trace": "import ipdb; ipdb.set_trace()",
    }
)

# TODO: defined function
# TODO: defined class
# TODO: python-ast
# TODO: don't overload tab for quinn snippet navigation
