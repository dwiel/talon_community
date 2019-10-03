# Talon voice commands for interacting with Adobe Lightroom
# John S. Cooper  jcooper@korgrd.com

from talon.voice import Key, Context

ctx = Context("Lightroom", bundle="com.adobe.Lightroom6")

ctx.keymap(
    {
        "import": Key("shift-cmd-i"),
        "show in finder": Key("cmd-r"),
        "grid [view]": Key("g"),
        "loop [view]": Key("e"),
        "compare [view]": Key("c"),
        "develop [view]": Key("d"),
        "grid [view]": Key("g"),
        "grid zoom in": Key("="),
        "grid zoom out": Key("-"),
        "(show | hide) toolbar": Key("t"),
        "crop": Key("r"),
        "crop": Key("r"),
        "next photo": Key("cmd-right"),
        "(preev | previous) photo": Key("cmd-left"),
        "zoom": Key("z"),
        "zoom": Key("z"),
        "(rating 1 | 1 star)": Key("1"),
        "(rating 2 | 2 stars)": Key("2"),
        "(rating 3 | 3 stars)": Key("3"),
        "(rating 4 | 4 stars)": Key("4"),
        "(rating 5 | 5 stars)": Key("5"),
        "color red": Key("6"),
        "color yellow": Key("7"),
        "color green": Key("8"),
        "color blue": Key("9"),
        "reject": Key("x"),
        "flag it": Key("`"),
        "unflag it": Key("u"),
        "rotate (left | counter clockwise)": Key("cmd-["),
        "rotate (right | clockwise)": Key("cmd-]"),
        "keywords": Key("cmd-k"),
        "auto tone": Key("cmd-u"),
        "auto white balance": Key("shift-cmd-u"),
        "black and white": Key("v"),
    }
)
