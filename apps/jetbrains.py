import os

import requests
import talon.clip as clip
from talon import ctrl
from talon.ui import active_app
from talon.voice import Context, Key

from ..utils import optional_numerals, text, text_to_number, text_to_range

try:
    from ..text.homophones import all_homophones

    # Map from every homophone back to the row it was in.
    homophone_lookup = {
        item.lower(): words for canon, words in all_homophones.items() for item in words
    }
except ImportError:
    homophone_lookup = {"right": ["right", "write"], "write": ["right", "write"]}
    all_homophones = homophone_lookup.keys()

try:
    from ..misc.mouse import delayed_click
except ImportError:
    print("Fallback mouse click logic")

    def delayed_click():
        ctrl.mouse_click(button=0)


# Each IDE gets its own port, as otherwise you wouldn't be able
# to run two at the same time and switch between them.
# Note that MPS and IntelliJ ultimate will conflict...
port_mapping = {
    "com.jetbrains.intellij": 8653,
    "com.jetbrains.intellij.ce": 8654,
    "com.jetbrains.AppCode": 8655,
    "com.jetbrains.CLion": 8657,
    "com.jetbrains.datagrip": 8664,
    "com.jetbrains.goland": 8659,
    "com.jetbrains.PhpStorm": 8662,
    "com.jetbrains.pycharm": 8658,
    "com.jetbrains.rider": 8660,
    "com.jetbrains.rubymine": 8661,
    "com.jetbrains.WebStorm": 8663,
    "com.google.android.studio": 8652,
}


def _get_nonce(port):
    try:
        with open(os.path.join("/tmp", "vcidea_" + str(port)), "r") as fh:
            return fh.read()
    except IOError:
        return None


def send_idea_command(cmd):
    print("Sending {}".format(cmd))
    bundle = active_app().bundle
    port = port_mapping.get(bundle, None)
    nonce = _get_nonce(port)
    if port and nonce:
        response = requests.get(
            "http://localhost:{}/{}/{}".format(port, nonce, cmd), timeout=(0.05, 3.05)
        )
        response.raise_for_status()
        return response.text


def get_idea_location():
    return send_idea_command("location").split()


def idea(cmd):
    return lambda _: send_idea_command(cmd)


def idea_num(cmd, drop=1, zero_okay=False):
    def handler(m):
        # noinspection PyProtectedMember
        line = text_to_number(m._words[drop:])
        print(cmd.format(line))
        if int(line) == 0 and not zero_okay:
            print("Not sending, arg was 0")
            return

        send_idea_command(cmd.format(line))

    return handler


def idea_range(cmd, drop=1):
    def handler(m):
        # noinspection PyProtectedMember
        start, end = text_to_range(m._words[drop:])
        print(cmd.format(start, end))
        send_idea_command(cmd.format(start, end))

    return handler


def idea_words(cmd, join=" "):
    def handler(m):
        # noinspection PyProtectedMember
        args = [str(w) for w in m.dgndictation[0]._words]
        print(args)
        send_idea_command(cmd.format(join.join(args)))

    return handler


def idea_find(direction):
    def handler(m):
        # noinspection PyProtectedMember
        args = [str(w) for w in m.dgndictation[0]._words]
        search_string = " ".join(args)
        cmd = "find {} {}"
        if len(args) == 1:
            word = args[0]
            if word in homophone_lookup:
                search_string = "({})".format("|".join(homophone_lookup[word]))
        print(args)
        send_idea_command(cmd.format(direction, search_string))

    return handler


def grab_identifier(m):
    old_clip = clip.get()
    # noinspection PyProtectedMember
    times = text_to_number(m._words[1:])  # hardcoded prefix length?
    if not times:
        times = 1
    try:
        old_line, old_col = get_idea_location()
        delayed_click(m, button=0, times=2)
        for _ in range(times - 1):
            send_idea_command("action EditorSelectWord")
        send_idea_command("action EditorCopy")
        send_idea_command("goto {} {}".format(old_line, old_col))
        send_idea_command("action EditorPaste")
    finally:
        clip.set(old_clip)


def is_real_jetbrains_editor(app, window):
    if app.bundle not in port_mapping:
        return False
    # XXX Expose "does editor have focus" as plugin endpoint.
    # XXX Window title empty in full screen.
    return "[" in window.title or len(window.title) == 0


# group = ContextGroup("jetbrains")
ctx = Context("jetbrains", func=is_real_jetbrains_editor)  # , group=group)

ctx.keymap(
    {
        "complete": idea("action CodeCompletion"),
        "smarter": idea("action SmartTypeCompletion"),
        "finish": idea("action EditorCompleteStatement"),
        "zoom": idea("action HideAllWindows"),
        "find (usage | usages)": idea("action FindUsages"),
        "(refactor | reflector) [<dgndictation>]": [
            idea("action Refactorings.QuickListPopupAction"),
            text,
        ],
        "fix [this]": idea("action ShowIntentionActions"),
        "fix next [error]": [
            idea("action GotoNextError"),
            idea("action ShowIntentionActions"),
        ],
        "fix previous [error]": [
            idea("action GotoPreviousError"),
            idea("action ShowIntentionActions"),
        ],
        "visit declaration": idea("action GotoDeclaration"),
        "visit (implementers | implementations)": idea("action GotoImplementation"),
        "visit type": idea("action GotoTypeDeclaration"),
        "(select previous | trail) <dgndictation>": idea_find("prev"),
        "(select next | crew) <dgndictation>": idea_find("next"),
        "search everywhere [for] [<dgndictation>]": [
            idea("action SearchEverywhere"),
            text,
        ],
        "search [for] [<dgndictation>]": [idea("action Find"), text],
        "search [for] this": idea("action FindWordAtCaret"),
        "next result": idea("action FindNext"),
        "(last | previous) result": idea("action FindPrevious"),
        "surround [this] [<dgndictation>]": [idea("action SurroundWith"), text],
        "generate [<dgndictation>]": [idea("action Generate"), text],
        "template [<dgndictation>]": [idea("action InsertLiveTemplate"), text],
        "select less": idea("action EditorUnSelectWord"),
        "select more": idea("action EditorSelectWord"),
        f"select (lines | line) {optional_numerals}": [
            idea_num("goto {} 0", drop=2),
            idea("action EditorLineStart"),
            idea("action EditorLineEndWithSelection"),
        ],
        "select block": [
            idea("action EditorCodeBlockStart"),
            idea("action EditorCodeBlockEndWithSelection"),
        ],
        "select this line": [
            idea("action EditorLineStart"),
            idea("action EditorLineEndWithSelection"),
        ],
        f"select lines {optional_numerals} until {optional_numerals}": idea_range(
            "range {} {}", drop=2
        ),
        f"select until {optional_numerals}": idea_num("extend {}", drop=2),
        f"(go | jump) to end of {optional_numerals}": idea_num("goto {} 9999", drop=4),
        "(clean | clear) line": [
            idea("action EditorLineEnd"),
            idea("action EditorDeleteToLineStart"),
        ],
        "(delete | remove) line": idea(
            "action EditorDeleteLine"
        ),  # xxx optional line number
        "(delete | clear) to end": idea("action EditorDeleteToLineEnd"),
        "(delete | clear) to start": idea("action EditorDeleteToLineStart"),
        "drag up": idea("action MoveLineUp"),
        "drag down": idea("action MoveLineDown"),
        "duplicate": idea("action EditorDuplicate"),
        "(go | jump) back": idea("action Back"),
        "(go | jump) forward": idea("action Forward"),
        "(synchronizing | synchronize)": idea("action Synchronize"),
        "comment": idea("action CommentByLineComment"),
        "(action | please) [<dgndictation>]": [idea("action GotoAction"), text],
        f"(go to | jump to) {optional_numerals}": idea_num("goto {} 0", drop=2),
        f"clone line {optional_numerals}": idea_num("clone {}", drop=2),
        f"grab {optional_numerals}": grab_identifier,
        "(start | stop) recording": idea("action StartStopMacroRecording"),
        "edit (recording | recordings)": idea("action EditMacros"),
        "play recording": idea("action PlaybackLastMacro"),
        "play recording <dgndictation>": [
            idea("action PlaySavedMacrosAction"),
            text,
            Key("enter"),
        ],
        "show (mark | marks | bookmark | bookmarks)": idea("action ShowBookmarks"),
        "[toggle] (mark | bookmark)": idea("action ToggleBookmark"),
        "next (mark | bookmark)": idea("action GotoNextBookmark"),
        "(last | previous) (mark | bookmark)": idea("action GotoPreviousBookmark"),
        f"(mark | bookmark) (0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9)": idea_num(
            "action ToggleBookmark{}", drop=1, zero_okay=True
        ),
        f"(jump | go) (mark | bookmark) (0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9)": idea_num(
            "action GotoBookmark{}", drop=2, zero_okay=True
        ),
    }
)
# group.load()
