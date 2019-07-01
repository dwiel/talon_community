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
        "[(edit | change)] current commit message": Key("cmd-shift-6"),
        "(edit | change) commit message": Key("f2"),
        "(edit | change) last commit message": Key("shift-f2"),
        "check out branch": Key("cmd-g"),
        "add branch": Key("f7"),
        "add tag": Key("shift-f7"),
        "stage": Key("cmd-t"),
        "filter files": Key("cmd-f"),
        "stash all": Key("cmd-s"),
        "apply stash": Key("shift-cmd-s"),
        "unstage": Key("shift-cmd-t"),
        "undo last commit": Key("shift-cmd-k"),
        "(show | hide) unchanged files": Key("cmd-1"),
        "(show | hide) unversioned files": Key("cmd-2"),
        "(show | hide) ignored files": Key("cmd-3"),
        "(show | hide) staged files": Key("cmd-4"),
        "next change": Key("f6"),
        "(previous | preev) change": Key("shift-f6"),
        "toggle compact changes": Key("cmd-."),
        "normal mode": Key("alt-cmd-1"),
        "review mode": Key("alt-cmd-2"),
        "clear output": Key("cmd-backspace"),
    }
)
