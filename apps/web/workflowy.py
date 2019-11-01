from talon.voice import Context, Key

from . import browser

ctx = Context(
    "workflowy", func=browser.url_matches_func("(https://)?workflowy.com/#/.*")
)
ctx.keymap(
    {
        "move up": Key("cmd-shift-up"),
        "move down": Key("cmd-shift-down"),
        "collapse": Key("cmd-up"),
        "expand": Key("cmd-down"),
        "snipline": Key("cmd-shift-delete"),
    }
)
