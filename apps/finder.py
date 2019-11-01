from talon.voice import Key, Context, Str, press


def go_to_path(path):
    def path_function(m):
        press("cmd-shift-g")
        Str(path)(None)
        press("return")

    return path_function


def context(app, win):
    if app.bundle == "com.apple.finder":
        return True
    # allow these commands to work while using open dialogue in atom. There is
    # probably a better way to do this more generally
    elif app.bundle == "com.github.atom" and win.title == "Open Folder":
        return True
    else:
        return False


ctx = Context("Finder", func=context)

ctx.keymap(
    {
        # actions
        # "select all": Key("cmd-a"),
        # "copy": Key("cmd-c"),
        # "cut": Key("cmd-x"),
        # "paste": Key("cmd-v"),
        "duplicate": Key("cmd-d"),
        "eject": Key("cmd-e"),
        "(search | find)": Key("cmd-f"),
        "hide [finder]": Key("cmd-h"),
        "hide (others | else)": Key("cmd-alt-h"),
        "(hide | no) toolbar": Key("cmd-alt-t"),
        "info": Key("cmd-i"),
        "view [options]": Key("cmd-j"),
        "connect [to server]": Key("cmd-k"),
        "[(make | create)] (alias | shortcut)": Key("cmd-l"),
        "minimize": Key("cmd-m"),
        "new window": Key("cmd-n"),
        "new folder": Key("cmd-shift-n"),
        # NOT WORKING "new smart folder": Key("cmd-alt-n"),
        "collapse": Key("cmd-left"),
        "expand": Key("cmd-right"),
        "open": Key("cmd-down"),
        "[show] original": Key("cmd-r"),
        "add to side bar": Key("cmd-t"),
        "trash it": Key("cmd-backspace"),
        "new tab": Key("cmd-alt-o"),
        "close": Key("cmd-w"),
        "undo": Key("cmd-z"),
        "[finder] preferences": Key("cmd-,"),
        "(icon | icons) [(mode | view)]": Key("cmd-1"),
        "list [(mode | view)]": Key("cmd-2"),
        "(column | columns) [(mode | view)]": Key("cmd-3"),
        "cover [flow] [(mode | view)]": Key("cmd-4"),
        "help": Key("cmd-?"),
        # navigation
        "back": Key("cmd-["),
        "(forward | next)": Key("cmd-]"),
        "(up | (parent [folder]))": Key("cmd-up"),
        "(cycle | switch) [window]": Key("cmd-`"),
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
        # NOT WORKING "(delete | empty) trash": Key("cmd-shift-del"),
        "spotlight [menu]": Key("cmd-space"),
        "spotlight window": Key("cmd-alt-space"),
        # NOT WORKING: Function key shorcuts (f8 through f12)
        "toggle hidden files": Key("cmd-shift-."),
        # the following require addition of keyboard shortcuts in System Preferences
        "zip it": Key("cmd-shift-z"),
        "show package contents": Key("cmd-alt-o"),
    }
)
