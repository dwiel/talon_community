import re

from talon.voice import Context, Key, press

from ..utils import is_filetype, snake_text, insert

FILETYPES = (".py",)

# ctx = Context("python", func=is_filetype(FILETYPES))
ctx = Context("python")
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
    insert(f"raise {exceptions[m['python.exception'][0]]}()")
    press("left")


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
        "raise value error": ["raise ValueError()", Key("left")],
        "raise not implemented error": "raise NotImplementedError()",
        "raise {python.exception}": raise_exception,
    }
)
ctx.set_list("exception", exceptions.keys())

# TODO: defined function
# TODO: defined class
# TODO: python-ast
# TODO: don't overload tab for quinn snippet navigation
