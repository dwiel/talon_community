# Talon voice commands for safari
# John S. Cooper  jcooper@korgrd.com

from talon.voice import Key, Context

ctx = Context("safari", bundle="com.apple.Safari")
ctx.keymap(
    {
        "(address bar | goto)": Key("cmd-l"),
        "add bookmark": Key("cmd-d"),
        "edit bookmarks": Key("alt-cmd-b"),
        "go (fore | forward)": Key("cmd-]"),
        "go back": Key("cmd-["),
        "go home": Key("cmd-shift-h"),
        "[(show | hide)] overview": Key("shift-cmd-\\"),
        "[(show | hide)] downloads": Key("alt-cmd-l"),
        "[(show | hide)] favorites": Key("shift-cmd-b"),
        "[show] first tab": Key("cmd-1"),
        "[show] second tab": Key("cmd-2"),
        "[show] third tab": Key("cmd-3"),
        "[show] fourth tab": Key("cmd-4"),
        "[show] fifth tab": Key("cmd-5"),
        "[show] (six | sixth) tab": Key("cmd-6"),
        "[show] seventh tab": Key("cmd-7"),
        "[show] eighth tab": Key("cmd-8"),
        "[show] last tab": Key("cmd-9"),
        "(reload | refresh)": Key("cmd-r"),
        "(show | hide) history": Key("cmd-y"),
        "reopen last tab": Key("cmd-shift-t"),
        "zoom in": Key("cmd-+"),
        "zoom out": Key("cmd--"),
        "[(enter | exit)] full screen": Key("ctrl-cmd-f"),
        # useful for Polyglot translation extension
        "translate": Key("ctrl-`"),
    }
)
