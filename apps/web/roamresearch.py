from talon.voice import Context, Key

from . import browser

ctx = Context(
    "roamresearch", func=browser.url_matches_func("(https://)?roamresearch.com/#/.*")
)
ctx.keymap(
    {
        "move up": Key("cmd-shift-up"),
        "move down": Key("cmd-shift-down"),
        "collapse": Key("cmd-up"),
        "expand": Key("cmd-down"),
        # "snipline": Key("cmd-shift-backspace"),
    }
)
