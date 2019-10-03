# Talon voice commands for interacting with 1password
# John S. Cooper  jcooper@korgrd.com

from talon.voice import Key, Context

ctx = Context("1password", bundle="com.agilebits.onepassword4")

ctx.keymap(
    {
        "new login": Key("shift-cmd-n"),
        "fill it": Key("alt-cmd-enter"),
        "duplicate": Key("cmd-d"),
        "edit": Key("cmd-e"),
        "copy password": Key("shift-cmd-c"),
        "[show] next category": Key("cmd-}"),
        "[show] (preev | previous) category": Key("cmd-{"),
    }
)
