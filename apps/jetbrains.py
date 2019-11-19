import os
import os.path
import time

import requests
import talon.clip as clip
from talon import ctrl
from talon.ui import active_app
from talon.voice import Context, Key, Str

from .jetbrains_psi import PSI_PATHS

from ..misc.basic_keys import alphabet
from .. import utils
from ..text.homophones import raise_homophones

from ..text.formatters import CAMELCASE, formatted_text

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

    def delayed_click(m, button=0, times=1, from_end=False, mods=None):
        if mods is None:
            mods = []
        for key in mods:
            ctrl.key_press(key, down=True)
        ctrl.mouse_click(button=button, times=times)
        for key in mods[::-1]:
            ctrl.key_press(key, up=True)
        time.sleep(0.032)


# Each IDE gets its own port, as otherwise you wouldn't be able
# to run two at the same time and switch between them.
# Note that MPS and IntelliJ ultimate will conflict...
port_mapping = {
    "com.jetbrains.intellij": 8653,
    "com.jetbrains.intellij-EAP": 8653,
    "com.jetbrains.intellij.ce": 8654,
    "com.jetbrains.AppCode": 8655,
    "com.jetbrains.CLion": 8657,
    "com.jetbrains.datagrip": 8664,
    "com.jetbrains.goland": 8659,
    "com.jetbrains.goland-EAP": 8659,
    "com.jetbrains.PhpStorm": 8662,
    "com.jetbrains.pycharm": 8658,
    "com.jetbrains.rider": 8660,
    "com.jetbrains.rubymine": 8661,
    "com.jetbrains.WebStorm": 8663,
    "com.google.android.studio": 8652,
}

extendCommands = []
toHereCommands = []
old_line, old_col = 0, 0
location_stack = []


def set_extend(*commands):
    def set_inner(_):
        global extendCommands
        extendCommands = commands

    return set_inner


def extend_action(m):
    global extendCommands
    # noinspection PyProtectedMember
    count = max(utils.text_to_number([utils.parse_word(w) for w in m._words[1:]]), 1)
    for _ in range(count):
        for cmd in extendCommands:
            send_idea_command(cmd)


def set_to_here(*commands):
    global toHereCommands, old_line, old_col
    old_line, old_col = get_idea_location()
    toHereCommands = commands


def to_here(m):
    global toHereCommands
    for cmd in toHereCommands:
        cmd(m)
    toHereCommands = []


def _get_nonce(port):
    try:
        with open(os.path.join("/tmp", "vcidea_" + str(port)), "r") as fh:
            return fh.read()
    except IOError:
        return None


def send_idea_command(cmd):
    # print("Sending {}".format(cmd))
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


def idea(*commands):
    def inner(_):
        global extendCommands
        extendCommands = commands
        for cmd in commands:
            send_idea_command(cmd)

    return inner


def idea_num(cmd, drop=1, zero_okay=False):
    def handler(m):
        # noinspection PyProtectedMember
        line = utils.text_to_number(m._words[drop:])
        # print(cmd.format(line))
        if int(line) == 0 and not zero_okay:
            print("Not sending, arg was 0")
            return

        send_idea_command(cmd.format(line))
        global extendCommands
        extendCommands = []

    return handler


# XXX Placeholder until I add an RPC template command to the backend
def start_template(key):
    send_idea_command("action InsertLiveTemplate")
    time.sleep(0.3)
    Str(key + "\n")(None)
    time.sleep(0.2)
    Key("enter")


def send_psi(path, cmd, index):
    if path not in PSI_PATHS:
        return
    path = PSI_PATHS[path].get(extension, PSI_PATHS[path].get("default", None))
    if path is None:
        return
    cmd_string = f"psi {cmd} {path}"
    if "##" in cmd_string:
        cmd_string = cmd_string.replace("##", f"%23{index}")
    else:
        cmd_string = f"{cmd_string}%23{index}"

    send_idea_command(cmd_string)


def idea_psi(cmd):
    def handler(m):
        generic_path = m["jetbrains.path"][0]
        index = PSI_PATHS[generic_path]["_"]
        try:
            index = utils.ordinal_indexes[m["jetbrains.ordinal"][0]]
        except KeyError:
            pass
        # print(cmd.format(line))
        send_psi(generic_path, cmd, index)
        global extendCommands
        extendCommands = []

    return handler


def idea_psi_and_snippet():
    def handler(m):
        path = m["jetbrains.path"][0]
        default_index = PSI_PATHS[path]["_"]
        how_to_add = PSI_PATHS[path].get("+", None)
        if how_to_add is None:
            return
        if PSI_PATHS[path].get(extension, None) is None:
            # Probably won't do the right thing with fallback path.
            return
        prefix, template = how_to_add
        try:
            default_index = utils.ordinal_indexes[m["jetbrains.ordinal"][0]]
        except KeyError:
            pass
        # print(cmd.format(line))
        index = default_index
        cmd = "end"
        if index == 0:
            index = -1
        if index != "next":
            # The "next" motion generally means we should add at point.
            send_psi(path, cmd, index)
        if prefix:
            Key(prefix)(None)
            time.sleep(0.1)
        if template:
            start_template(template)
        try:
            # noinspection PyProtectedMember
            if m.dgndictation[0]._words:
                time.sleep(0.1)
                formatted_text(CAMELCASE)(m)
        except AttributeError:
            pass

        global extendCommands
        extendCommands = []

    return handler


def idea_range(cmd, drop=1):
    def handler(m):
        # noinspection PyProtectedMember
        start, end = utils.text_to_range(m._words[drop:])
        # print(cmd.format(start, end))
        send_idea_command(cmd.format(start, end))
        global extendCommands
        extendCommands = []

    return handler


def idea_find(direction):
    def handler(m):
        # noinspection PyProtectedMember
        args = utils.parse_words(m)
        search_string = " ".join(args)
        cmd = "find {} {}"
        if len(args) == 1:
            word = args[0]
            if word in homophone_lookup:
                search_string = "({})".format("|".join(homophone_lookup[word]))
        # print(args)
        send_idea_command(cmd.format(direction, search_string))
        global extendCommands
        extendCommands = [cmd.format(direction, search_string)]

    return handler


def idea_bounded(direction):
    def handler(m):
        # noinspection PyProtectedMember
        print("hello")
        keys = [alphabet[k] for k in m["jetbrains.alphabet"]]
        search_string = "%5Cb" + r"%5B^-_ .()%5D*?".join(
            keys
        )  # URL escaped Java regex! '\b' 'A[%-_.()]*?Z"
        cmd = "find {} {}"
        print(keys, search_string, cmd)
        send_idea_command(cmd.format(direction, search_string))
        global extendCommands
        extendCommands = [cmd.format(direction, search_string)]

    return handler


def grab_identifier(m):
    old_clip = clip.get()
    # noinspection PyProtectedMember
    times = utils.text_to_number(m._words[1:])  # hardcoded prefix length?
    if not times:
        times = 1
    try:
        original_line, original_column = get_idea_location()
        delayed_click(m, button=0, times=2)
        for _ in range(times - 1):
            send_idea_command("action EditorSelectWord")
        send_idea_command("action EditorCopy")
        send_idea_command("goto {} {}".format(original_line, original_column))
        send_idea_command("action EditorPaste")
    finally:
        clip.set(old_clip)


extension = None


def is_real_jetbrains_editor(app, window):
    global extension
    if app.bundle not in port_mapping:
        return False
    if window is None:
        return False
    # XXX Expose "does editor have focus" as plugin endpoint.
    # XXX Window title empty in full screen.
    title = window.title
    filename = title.split(" - ")[-1]
    filename = filename.split(" [")[0]
    extension = os.path.splitext(filename)[1][1:]

    return "[" in window.title or len(window.title) == 0


def push_loc(_):
    line, col = get_idea_location()
    global location_stack
    location_stack.append((line, col))


def pop_loc(_):
    global location_stack
    if not location_stack:
        return
    line, col = location_stack.pop()
    send_idea_command("goto {} {}".format(line, col))


def swap_loc(_):
    global location_stack
    if not location_stack:
        return
    line1, col1 = get_idea_location()
    line2, col2 = location_stack.pop()
    send_idea_command("goto {} {}".format(line2, col2))
    location_stack.append((line1, col1))


def phones_selection(m):
    raise_homophones(m, is_selection=True)


select_verbs = {
    "select": [],
    "copy": [idea("action EditorCopy")],
    "cut": [idea("action EditorCut")],
    "clear": [idea("action EditorBackSpace")],
    "comment": [idea("action CommentByLineComment")],
    "expand": [idea("action ExpandRegion")],
    "collapse": [idea("action CollapseRegion")],
    "phones": [phones_selection],
    "refactor": [idea("action Refactorings.QuickListPopupAction")],
    "rename": [idea("action RenameElement")],
}

select_objects = {
    "here": [
        lambda m: delayed_click(m, from_end=True),
        idea("action EditorLineStart", "action EditorLineEndWithSelection"),
    ],
    "region": [],
    "this": [idea("action EditorSelectWord")],
    "phrase": [utils.select_last_insert],
    "last <dgndictation> [over]": [idea_find("prev")],
    "next <dgndictation> [over]": [idea_find("next")],
    "last bounded {jetbrains.alphabet}+": [idea_bounded("prev")],
    "next bounded {jetbrains.alphabet}+": [idea_bounded("next")],
    "line": [
        idea("action EditorLineStart", "action EditorLineEndWithSelection"),
        set_extend(
            "action EditorLineStart",
            "action EditorLineStart",
            "action EditorLineEndWithSelection",
        ),
    ],
    f"line {utils.numerals}": [
        idea_num("goto {} 0", drop=2),  # broken with go start
        idea("action EditorLineStart", "action EditorLineEndWithSelection"),
        set_extend(
            "action EditorLineStart",
            "action EditorLineStart",
            "action EditorLineEndWithSelection",
        ),
    ],
    f"lines {utils.numerals} until {utils.numerals}": [
        idea_range("range {} {}", drop=2)
    ],  # broken with go start
    f"until line {utils.numerals}": [
        idea_num("extend {}", drop=3)
    ],  # broken with go start
    # Structure
    "[{jetbrains.ordinal}] {jetbrains.path}": [push_loc, idea_psi("select")],
    # Generic Editor
    "all": [idea("action $SelectAll")],
    "left": [idea("action EditorLeftWithSelection")],
    "right": [idea("action EditorRightWithSelection")],
    "up": [idea("action EditorUpWithSelection")],
    "down": [idea("action EditorDownWithSelection")],
    "word left": [idea("action EditorPreviousWordWithSelection")],
    "word right": [idea("action EditorNextWordWithSelection")],
    "camel left": [idea("action EditorPreviousWordInDifferentHumpsModeWithSelection")],
    "camel right": [idea("action EditorNextWordInDifferentHumpsModeWithSelection")],
    "way left": [idea("action EditorLineStartWithSelection")],
    "way right": [idea("action EditorLineEndWithSelection")],
    "way up": [idea("action EditorTextStartWithSelection")],
    "way down": [idea("action EditorTextEndWithSelection")],
}

movement_verbs = {"go": [], "fix": [idea("action ShowIntentionActions")]}

movement_objects = {
    "this": [],
    "here": [lambda m: delayed_click(m, from_end=True)],
    "next (error | air)": [idea("action GotoNextError")],
    "last (error | air)": [idea("action GotoPreviousError")],
    "last <dgndictation> [over]": [idea_find("prev"), idea("action EditorRight")],
    "next <dgndictation> [over]": [idea_find("next"), idea("action EditorRight")],
    "last bounded {jetbrains.alphabet}+": [
        idea_bounded("prev"),
        idea("action EditorRight"),
    ],
    "next bounded {jetbrains.alphabet}+": [
        idea_bounded("next"),
        idea("action EditorRight"),
    ],
    f"line start {utils.numerals}": [idea_num("goto {} 0", drop=3)],
    f"line end {utils.numerals}": [idea_num("goto {} 9999", drop=3)],
    # This will put the cursor past the indentation
    f"line {utils.numerals}": [
        idea_num("goto {} 9999", drop=2),
        idea("action EditorLineEnd"),
        idea("action EditorLineStart"),
        set_extend(),
    ],
    # Structural
    "[end] [{jetbrains.ordinal}] {jetbrains.path}": [push_loc, idea_psi("end")],
    "start [{jetbrains.ordinal}] {jetbrains.path}": [push_loc, idea_psi("start")],
    # Generic
    "phrase": [utils.select_last_insert, idea("action EditorLeft")],
    "left": [idea("action EditorLeft")],
    "right": [idea("action EditorRight")],
    "up": [idea("action EditorUp")],
    "down": [idea("action EditorDown")],
    "word left": [idea("action EditorPreviousWord")],
    "word right": [idea("action EditorNextWord")],
    "camel left": [idea("action EditorPreviousWordInDifferentHumpsMode")],
    "camel right": [idea("action EditorNextWordInDifferentHumpsMode")],
    "way left": [idea("action EditorLineStart")],
    "way right": [idea("action EditorLineEnd")],
    "way up": [idea("action EditorTextStart")],
    "way down": [idea("action EditorTextEnd")],
}


def build_text_action_keymap():
    keymap = {}
    for verb, verb_actions in select_verbs.items():  # Dict comprehension?
        for obj, obj_actions in select_objects.items():
            keymap[f"{verb} {obj}"] = obj_actions + verb_actions
    for verb, verb_actions in movement_verbs.items():  # Dict comprehension?
        for obj, obj_actions in movement_objects.items():
            keymap[f"{verb} {obj}"] = obj_actions + verb_actions
    return keymap


keymap = build_text_action_keymap()

# group = ContextGroup("jetbrains")
ctx = Context("jetbrains", func=is_real_jetbrains_editor)  # , group=group)
keymap.update(
    {
        # Misc verbs
        "complete": [idea("action CodeCompletion")],
        "perfect": [
            idea("action CodeCompletion", "action CodeCompletion")
        ],  # perfect == extra complete
        "smart": [idea("action SmartTypeCompletion")],
        # Variants which take text?  Replaced mostly with "call" formatter.
        # "complete <dgndictation> [over]": [idea("action CodeCompletion"), text],
        # "smart <dgndictation> [over]": [idea("action SmartTypeCompletion"), text],
        "finish": idea("action EditorCompleteStatement"),
        "done": idea("action EditorCompleteStatement"),
        "toggle tools": idea("action HideAllWindows"),
        "drag up": idea("action MoveLineUp"),
        "drag down": idea("action MoveLineDown"),
        "clone this": idea("action EditorDuplicate"),
        "clone line": idea("action EditorDuplicate"),
        f"clone line {utils.numerals}": [idea_num("clone {}", drop=2)],
        f"grab {utils.optional_numerals}": [grab_identifier, set_extend()],
        # "(synchronizing | synchronize)": idea("action Synchronize"),
        "(action | please)": idea("action GotoAction"),
        "(action | please) <dgndictation>++ [over]": [
            idea("action GotoAction"),
            utils.text,
        ],
        f"extend {utils.optional_numerals}": extend_action,
        # Refactoring
        "refactor": idea("action Refactorings.QuickListPopupAction"),
        "refactor <dgndictation> [over]": [
            idea("action Refactorings.QuickListPopupAction"),
            utils.text,
        ],
        "extract variable": idea("action IntroduceVariable"),
        "extract field": idea("action IntroduceField"),
        "extract constant": idea("action IntroduceConstant"),
        "extract parameter": idea("action IntroduceParameter"),
        "extract interface": idea("action ExtractInterface"),
        "extract method": idea("action ExtractMethod"),
        # Quick Fix / Intentions
        "fix this <dgndictation> [over]": [
            idea("action ShowIntentionActions"),
            utils.text,
        ],
        "fix (format | formatting)": idea("action ReformatCode"),
        # Go: move the caret
        "(go declaration | follow)": idea("action GotoDeclaration"),
        "go implementation": idea("action GotoImplementation"),
        "go usage": idea("action FindUsages"),
        "go type": idea("action GotoTypeDeclaration"),
        "go test": idea("action GotoTest"),
        "go back": idea("action Back"),
        "go forward": idea("action Forward"),
        # Special Selects
        "select less": idea("action EditorUnSelectWord"),
        "select more": idea("action EditorSelectWord"),
        "select this": idea("action EditorSelectWord"),
        "multi-select up": idea("action EditorCloneCaretAbove"),
        "multi-select down": idea("action EditorCloneCaretBelow"),
        "multi-select fewer": idea("action UnselectPreviousOccurrence"),
        "multi-select more": idea("action SelectNextOccurrence"),
        "multi-select all": idea("action SelectAllOccurrences"),
        # Search
        "search (everywhere | all)": idea("action SearchEverywhere"),
        "search (everywhere | all) <dgndictation> [over]": [
            idea("action SearchEverywhere"),
            utils.text,
            set_extend(),
        ],
        "recent": [idea("action RecentFiles"), set_extend()],
        "recent <dgndictation> [over]": [
            idea("action RecentFiles"),
            utils.text,
            set_extend(),
        ],
        "search": idea("action Find"),
        "search for <dgndictation> [over]": [
            idea("action Find"),
            utils.text,
            set_extend("action FindNext"),
        ],
        # "go next search": idea("action FindNext"),
        # "go last search": idea("action FindPrevious"),
        "go next result": idea("action FindNext"),
        "go last result": idea("action FindPrevious"),
        "search in path": idea("action FindInPath"),
        "search in path <dgndictation> [over]": [idea("action FindInPath"), utils.text],
        "search this": idea("action FindWordAtCaret"),
        # Templates: surround, generate, template.
        # "surround [this] with": idea("action SurroundWith"),
        "surround [this] with <dgndictation> [over]": [
            idea("action SurroundWith"),
            utils.text,
        ],
        # Making these longer to reduce collisions with real code dictation.
        "insert generated <dgndictation> [over]": [idea("action Generate"), utils.text],
        "insert template <dgndictation> [over]": [
            idea("action InsertLiveTemplate"),
            utils.text,
        ],
        "create template": idea("action SaveAsTemplate"),
        # Lines / Selections
        "clear line contents": idea(
            "action EditorLineEnd", "action EditorDeleteToLineStart"
        ),
        # XXX Replaced with way left/right
        # "clear line end": idea("action EditorDeleteToLineEnd"),
        # "clear line start": idea("action EditorDeleteToLineStart"),
        # Run!
        "run menu": idea("action ChooseRunConfiguration"),
        "run again": idea("action Run"),
        # Recording
        "toggle recording": idea("action StartStopMacroRecording"),
        "change (recording | recordings)": idea("action EditMacros"),
        "play recording": idea("action PlaybackLastMacro"),
        "play recording <dgndictation> [over]": [
            idea("action PlaySavedMacrosAction"),
            utils.text,
            Key("enter"),
        ],
        # Talon Marks
        "pushed": push_loc,
        "popped": pop_loc,
        "swapped": swap_loc,
        # Marks
        "go mark": idea("action ShowBookmarks"),
        "toggle mark": idea("action ToggleBookmark"),
        "toggle mark here": [
            lambda m: delayed_click(m, from_end=True),
            idea("action ToggleBookmark"),
        ],
        "go next mark": idea("action GotoNextBookmark"),
        "go last mark": idea("action GotoPreviousBookmark"),
        f"toggle mark (0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9)": idea_num(
            "action ToggleBookmark{}", drop=1, zero_okay=True
        ),
        f"go mark (0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9)": idea_num(
            "action GotoBookmark{}", drop=2, zero_okay=True
        ),

        # Folding
        "expand deep": idea("action ExpandRegionRecursively"),
        "expand all": idea("action ExpandAllRegions"),
        "collapse deep": idea("action CollapseRegionRecursively"),
        "collapse all": idea("action CollapseAllRegions"),

        # Splits
        "split right": idea("action MoveTabRight"),
        "split down": idea("action MoveTabDown"),
        "split vertically": idea("action SplitVertically"),
        "split horizontally": idea("action SplitHorizontally"),
        "split flip": idea("action ChangeSplitOrientation"),
        "split window": idea("action EditSourceInNewWindow"),
        "clear split": idea("action Unsplit"),
        "clear all splits": idea("action UnsplitAll"),
        "go next split": idea("action NextSplitter"),
        "go last split": idea("action LastSplitter"),

        # miscellaneous
        # XXX These might be better than the structural ones, depending on language.
        # "go next (method | function)": idea("action MethodDown"),
        # "go last (method | function)": idea("action MethodUp"),

        # Clipboard
        # "clippings": idea("action PasteMultiple"),  # XXX Might be a long-lived action.  Replaced with Alfred.
        "copy path": idea("action CopyPaths"),
        "copy reference": idea("action CopyReference"),
        "copy pretty": idea("action CopyAsRichText"),

        # File Creation
        "create sibling": idea("action NewElementSamePlace"),
        "create sibling <dgndictation> [over]": [
            idea("action NewElementSamePlace"),
            utils.text,
        ],
        "create file": idea("action NewElement"),
        "create file <dgndictation> [over]": [idea("action NewElement"), utils.text],

        # Task Management
        "go task": [idea("action tasks.goto")],
        "go browser task": [idea("action tasks.open.in.browser")],
        "switch task": [idea("action tasks.switch")],
        "clear task": [idea("action tasks.close")],
        "fix task settings": [idea("action tasks.configure.servers")],

        # Git / Github (not using verb-noun-adjective pattern, mirroring terminal commands.)
        "jet pull": idea("action Vcs.UpdateProject"),
        "jet commit": idea("action CheckinProject"),
        "jet push": idea("action CheckinProject"),
        "jet log": idea("action Vcs.ShowTabbedFileHistory"),
        "jet browse": idea("action Github.Open.In.Browser"),
        "jet (gets | gist)": idea("action Github.Create.Gist"),
        "jet (pull request | request)": idea("action Github.Create.Pull.Request"),
        "jet (view | show | list) (requests | request)": idea(
            "action Github.View.Pull.Request"
        ),
        "jet (annotate | blame)": idea("action Annotate"),
        "jet menu": idea("action Vcs.QuickListPopupAction"),

        # Tool windows:
        # Toggling various tool windows
        "toggle project": idea("action ActivateProjectToolWindow"),
        "toggle find": idea("action ActivateFindToolWindow"),
        "toggle run": idea("action ActivateRunToolWindow"),
        "toggle debug": idea("action ActivateDebugToolWindow"),
        "toggle events": idea("action ActivateEventLogToolWindow"),
        "toggle terminal": idea("action ActivateTerminalToolWindow"),
        "toggle jet": idea("action ActivateVersionControlToolWindow"),
        "toggle structure": idea("action ActivateStructureToolWindow"),
        "toggle database": idea("action ActivateDatabaseToolWindow"),
        "toggle database changes": idea("action ActivateDatabaseChangesToolWindow"),
        "toggle make": idea("action ActivatemakeToolWindow"),
        "toggle to do": idea("action ActivateTODOToolWindow"),
        "toggle docker": idea("action ActivateDockerToolWindow"),
        "toggle favorites": idea("action ActivateFavoritesToolWindow"),
        "toggle last": idea("action JumpToLastWindow"),
        # Pin/dock/float
        "toggle pinned": idea("action TogglePinnedMode"),
        "toggle docked": idea("action ToggleDockMode"),
        "toggle floating": idea("action ToggleFloatingMode"),
        "toggle windowed": idea("action ToggleWindowedMode"),
        "toggle split": idea("action ToggleSideMode"),
        # Settings, not windows
        "toggle tool buttons": idea("action ViewToolButtons"),
        "toggle toolbar": idea("action ViewToolBar"),
        "toggle status [bar]": idea("action ViewStatusBar"),
        "toggle navigation [bar]": idea("action ViewNavigationBar"),
        # Active editor settings
        "toggle power save": idea("action TogglePowerSave"),
        "toggle whitespace": idea("action EditorToggleShowWhitespaces"),
        "toggle indents": idea("action EditorToggleShowIndentLines"),
        "toggle line numbers": idea("action EditorToggleShowLineNumbers"),
        "toggle bread crumbs": idea("action EditorToggleShowBreadcrumbs"),
        "toggle gutter icons": idea("action EditorToggleShowGutterIcons"),
        "toggle wrap": idea("action EditorToggleUseSoftWraps"),
        "toggle parameters": idea("action ToggleInlineHintsAction"),
        # Toggleable views
        "toggle fullscreen": idea("action ToggleFullScreen"),
        "toggle distraction [free mode]": idea("action ToggleDistractionFreeMode"),
        "toggle presentation [mode]": idea("action TogglePresentationMode"),

        # Tabs
        "go first tab": idea("action GoToTab1"),
        "go second tab": idea("action GoToTab2"),
        "go third tab": idea("action GoToTab3"),
        "go fourth tab": idea("action GoToTab4"),
        "go fifth tab": idea("action GoToTab5"),
        "go sixth tab": idea("action GoToTab6"),
        "go seventh tab": idea("action GoToTab7"),
        "go eighth tab": idea("action GoToTab8"),
        "go ninth tab": idea("action GoToTab9"),
        "go next tab": idea("action NextTab"),
        "go last tab": idea("action PreviousTab"),
        "go final tab": idea("action GoToLastTab"),
        "clear tab": idea("action CloseActiveTab"),


        # Quick popups
        "change scheme": idea("action QuickChangeScheme"),
        "toggle (doc | documentation)": idea("action QuickJavaDoc"),  # Always javadoc
        "pop (doc | documentation)": idea("action QuickJavaDoc"),  # Always javadoc
        "(pop deaf | toggle definition)": idea("action QuickImplementations"),
        "pop type": idea("action ExpressionTypeInfo"),
        "pop parameters": idea("action ParameterInfo"),

        # Breakpoints / debugging
        "go breakpoints": idea("action ViewBreakpoints"),
        "toggle [line] breakpoint": idea("action ToggleLineBreakpoint"),
        "toggle method breakpoint": idea("action ToggleMethodBreakpoint"),
        "step over": idea("action StepOver"),
        "step into": idea("action StepInto"),
        "step smart": idea("action SmartStepInto"),
        "step to line": idea("action RunToCursor"),

        # Grow / Shrink
        "(grow | shrink) window right": idea("action ResizeToolWindowRight"),
        "(grow | shrink) window left": idea("action ResizeToolWindowLeft"),
        "(grow | shrink) window up": idea("action ResizeToolWindowUp"),
        "(grow | shrink) window down": idea("action ResizeToolWindowDown"),

        # Dash Searching https://github.com/gdelmas/IntelliJDashPlugin
        "go [smart] dash": idea("action SmartSearchAction"),
        "go all dash": idea("action SearchAction"),

        # Most of the edition, selection, etc. commands now come
        # from build_text_action_keymap.  Any edge cases go here.

        # moving
        "go phrase left": [utils.select_last_insert, idea("action EditorLeft")],
        # clipboard
        "cut this": idea("action EditorCut"),
        "copy this": idea("action EditorCopy"),
        "paste [here]": idea("action EditorPaste"),
        # From here commands
        "select from here": lambda m: set_to_here(
            lambda _: delayed_click(m, from_end=True),
            lambda m2: delayed_click(m2, from_end=True, mods=["shift"]),
        ),
        "clear from here": [
            (
                lambda m: set_to_here(
                    lambda _: delayed_click(m, from_end=True),
                    lambda m2: delayed_click(m2, from_end=True, mods=["shift"]),
                    lambda _: time.sleep(0.2),
                    idea("action EditorBackSpace"),
                )
            )
        ],
        "comment from here": lambda m: set_to_here(
            lambda _: delayed_click(m, from_end=True),
            lambda m2: delayed_click(m2, from_end=True, mods=["shift"]),
            lambda _: time.sleep(0.2),
            idea("action CommentByLineComment"),
        ),
        "copy from here": lambda m: set_to_here(
            lambda _: delayed_click(m, from_end=True),
            lambda m2: delayed_click(m2, from_end=True, mods=["shift"]),
            lambda _: time.sleep(0.2),
            idea("action EditorCopy"),
        ),
        "cut from here": lambda m: set_to_here(
            lambda _: delayed_click(m, from_end=True),
            lambda m2: delayed_click(m2, from_end=True, mods=["shift"]),
            lambda _: time.sleep(0.2),
            idea("action EditorCut"),
        ),
        "to here": to_here,
        # Structure
        "create {jetbrains.path} [<dgndictation>] [over]": [
            push_loc,
            idea_psi_and_snippet(),
        ],
    }
)

ctx.keymap(keymap)
ctx.set_list("alphabet", alphabet.keys())
ctx.set_list("ordinal", utils.ordinal_indexes.keys())
ctx.set_list("path", PSI_PATHS.keys())

# group.load()
