from talon.voice import Key, Context, Str, press


def go_to_path(path):
    def path_function(m):
        press("cmd-shift-g")
        Str(path)(None)
        press("return")

    return path_function


ctx = Context("Finder", bundle="com.apple.finder")
ctx.keymap(
    {
        # actions
        "duplicate": Key("cmd-d"),
        "collapse": Key("cmd-left"),
        "expand": Key("cmd-right"),
        "open": Key("cmd-down"),
        "trash it": Key("cmd-backspace"),
        "show package contents": Key("cmd-alt-o"),
        # navigation
        "computer": Key("cmd-shift-c"),
        "desktop": Key("cmd-shift-d"),
        "all files": Key("cmd-shift-f"),
        "go to": Key("cmd-shift-g"),
        "home": Key("cmd-shift-h"),
        "icloud": Key("cmd-shift-i"),
        "documents": Key("cmd-shift-o"),
        "air drop": Key("cmd-shift-r"),
        "utilities": Key("cmd-shift-u"),
        "downloads": Key("cmd-shift-l"),
        "applications": Key("cmd-shift-a"),
        "developer": go_to_path("~/Developer"),
        "talon": go_to_path("~/.talon/user"),
    }
)
