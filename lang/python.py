from talon.voice import Context, Key


def python(app, win):
    return win.doc.endswith(".py")


ctx = Context("python", func=python)

ctx.keymap(
    {
        "state any": ["any()", Key("left")],
        "dunder in it": "__init__",  # TODO: move into python file
        "dot pie": ".py",
    }
)


# TODO: defined function
# TODO: defined class
# TODO: python-ast
# TODO: don't overload tab for quinn snippet navigation
