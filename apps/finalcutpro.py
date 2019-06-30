# Talon voice commands for interacting with final cut pro
# John S. Cooper  jcooper@korgrd.com

from talon.voice import Key, Context

ctx = Context("FinalCutPro", bundle="com.apple.FinalCut")

ctx.keymap(
    {
        "new event": Key("alt-n"),
        "new project": Key("cmd-n"),
        "(reveal | show) in browser": Key("shift-f"),
        "add marker": Key("m"),
        "blade [tool]": Key("b"),
        "(select | arrow) tool": Key("a"),
        "set duration": Key("ctrl-d"),
        "insert gap": Key("alt-f"),
        "lower volume": Key("ctrl--"),
        "raise volume": Key("ctrl-="),
        "import": Key("cmd-i"),
        "add transition": Key("cmd-t"),
        "play full screen": Key("cmd-shift-f"),
        "(show | hide) browser": Key("cmd-ctrl-1"),
        "(show | hide) timeline": Key("cmd-ctrl-2"),
        "(show | hide) inspector": Key("cmd-4"),
        "(show | hide) meters": Key("cmd-shift-8"),
        "(show | hide) transitions": Key("cmd-ctrl-5"),
        "(show | hide) effects": Key("cmd-5"),
    }
)
