import time

from talon.voice import Context, Key

from ..utils import text

ctx = Context("slack", bundle="com.tinyspeck.slackmacgap")

keymap = {
    # Channel
    "channel": Key("cmd-k"),
    "channel <dgndictation>": [
        Key("cmd-k"),
        lambda m: time.sleep(0.1),
        text,
        lambda m: time.sleep(0.1),
        Key("enter"),
    ],
    "channel last": Key("alt-up"),
    "([channel] unread last | gopreev)": Key("alt-shift-up"),
    "channel next": Key("alt-down"),
    "([channel] unread next | goneck)": Key("alt-shift-down"),
    "[channel] info": Key("cmd-shift-i"),
    "channel up": Key("alt-up"),
    "channel down": Key("alt-down"),
    # Navigation
    "move focus": Key("ctrl-`"),
    "next section": Key("f6"),
    "previous section": Key("shift-f6"),
    "page up": Key("pageup"),
    "page down": Key("pagedown"),
    "((open | collapse) right pane | toggle sidebar)": Key("cmd-."),
    "direct messages": Key("cmd-shift-k"),
    "(unread threads | new threads | threads)": Key("cmd-shift-t"),
    "(history [next] | go back | [go] backward | baxley)": Key("cmd-["),
    "(back to the future | ford | go forward | fourthly)": Key("cmd-]"),
    "next element": Key("tab"),
    "previous element": Key("shift-tab"),
    "(my stuff | activity)": Key("cmd-shift-m"),
    "toggle directory": Key("cmd-shift-e"),
    "(starred [items] | stars)": Key("cmd-shift-s"),
    "unread [messages]": Key("cmd-j"),
    "(go | undo | toggle) full": Key("ctrl-cmd-f"),
    # Messaging
    "grab left": Key("shift-up"),
    "grab right": Key("shift-down"),
    "add line": Key("shift-enter"),
    "(slaw | slapper)": [Key("cmd-right"), Key("shift-enter")],
    "(react | reaction)": Key("cmd-shift-\\"),
    "user": Key("@"),
    "tag channel": Key("#"),
    "(insert command | commandify)": Key("cmd-shift-c"),
    "insert code": [
        "``````",
        Key("left left left"),
        Key("shift-enter"),
        Key("shift-enter"),
        Key("up"),
    ],
    "(bullet | bulleted) list": Key("cmd-shift-8"),
    "(number | numbered) list": Key("cmd-shift-7"),
    "(quotes | quotation)": Key("cmd-shift->"),
    "bold": Key("cmd-b"),
    "(italic | italicize)": Key("cmd-i"),
    "(strike | strikethrough)": Key("cmd-shift-x"),
    "mark all read": Key("shift-esc"),
    "mark channel read": Key("esc"),
    # "clear": [Key("cmd-a"), Key("backspace")],
    # Files and Snippets
    "upload": Key("cmd-u"),
    "snippet": Key("cmd-shift-enter"),
    # Calls
    "([toggle] mute | unmute)": Key("m"),
    "([toggle] video)": Key("v"),
    "invite": Key("a"),
    # Miscellaneous
    "keyboard shortcuts": Key("cmd-/"),
    "set status": Key("cmd-shift-y"),
}

ctx.keymap(keymap)
