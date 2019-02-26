from talon.voice import Context, Key
import os

ctx = Context("system")

ctx.keymap(
    {
        "(prefies | preferences)": Key("cmd-,"),
        "put computer to sleep": lambda m: os.system("pmset sleepnow"),
        # Requires activation of System Preferences -> Shortcuts -> Input Sources
        # -> "Select the previous input source"
        "change language": Key("ctrl-space"),
    }
)
