# Talon voice commands for SmartGit
# John S. Cooper  jcooper@korgrd.com

from talon.voice import Key, Context

ctx = Context("smartgit", bundle="com.syntevo.smartgit")
ctx.keymap(
    {
        "commit [changes]": Key("cmd-k"),
        "undo last commit": Key("shift-cmd-k"),
        "pull it": Key("cmd-p"),
        "push it": Key("cmd-u"),
        "show log": Key("cmd-l"),
        "(edit | change) commit message": Key("f2"),
        "check out branch": Key("cmd-g"),
        "add branch": Key("f7"),
        "stage": Key("cmd-t"),
        "unstage": Key("shift-cmd-t"),
        "(show | hide) unchanged files": Key("cmd-1"),
    }
)
