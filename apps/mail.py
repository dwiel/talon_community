# Talon voice commands for interacting with macOS Mail
# John S. Cooper  jcooper@korgrd.com

from talon.voice import Key, Context

ctx = Context("mail", bundle="com.apple.mail")

ctx.keymap(
    {
        "new mail": Key("cmd-n"),
        "send mail": Key("cmd-shift-d"),
        "reply mail": Key("cmd-r"),
        "reply all": Key("cmd-shift-r"),
        "forward mail": Key("cmd-shift-f"),
        "mark (read | unread)": Key("cmd-shift-u"),
        "trash it": Key("backspace"),
    }
)
