import json
import time
import os

from talon import app, ctrl, tap, resource
from talon import dispatch
from talon.voice import Context

from ..utils import parse_words

SAVED_MACROS_FILENAME = os.path.join(os.path.dirname(__file__), "saved_macros.json")


class Macro:
    def __init__(self):
        self.recording = False
        self.log = []

        tap.register(tap.KEY | tap.MCLICK | tap.MMOVE | tap.SCROLL, self.on_event)

    def record(self):
        self.recording = True
        self.log = []

    def finish(self):
        self.recording = False
        log = self.log
        self.log = []
        return log

    def play(self, log, delay=True):
        for i, (typ, e) in enumerate(log):
            if i > 0 and delay:
                _, last = log[i - 1]
                time.sleep(max(e.ts - last.ts, 0))

            # if typ == tap.MMOVE:
            #     ctrl.mouse_move(e.x, e.y)
            # elif typ == tap.MCLICK:
            #     ctrl.mouse_click(button=e.button, down=e.down, up=e.up)
            if typ == tap.KEY and (e.down or e.up):
                mods = {mod: True for mod in e.mods}
                ctrl.key_press(e.key, down=e.down, up=e.up, **mods)
            # elif typ == tap.SCROLL:
            #     ctrl.mouse_scroll(x=e.x, y=e.y, by_lines=e.by_lines)

    def append(self, typ, e):
        if self.recording:
            self.log.append((typ, e))

    def on_event(self, typ, e):
        # if typ == tap.KEY and (e == 'f1' or e == 'f2' or e == 'f3'):
        #     return
        self.append(typ, e)


macro = Macro()
last_macro = None


def alias_stop(m):
    global last_macro
    last_macro = macro.finish()


def alias_play(m):
    alias_stop(m)
    macro.play(last_macro)


def alias_print(m):
    for i, (typ, e) in enumerate(last_macro):
        if typ == tap.KEY and e.down:
            mods = {mod: True for mod in e.mods}
            if not mods:
                print(e.key)


def alias_string():
    str = ""
    for i, (typ, e) in enumerate(last_macro):
        if typ == tap.KEY and e.down:
            mods = {mod: True for mod in e.mods}
            if not mods:
                str += e.key
    return str


def _load_saved_macros():
    try:
        with resource.open("saved_macros.json") as f:
            saved_macros = json.load(f)
        saved_macros = {k: v for k, v in saved_macros.items() if k}
        return saved_macros
    except Exception:
        return {}


def _save_new_macro(name, contents):
    if name and contents:
        existing_macros = _load_saved_macros()
        existing_macros[name] = contents
        with open(SAVED_MACROS_FILENAME, "w") as f:
            json.dump(existing_macros, f, indent=4)


def alias_save(m):
    global macro

    alias_stop(m)

    _save_new_macro(" ".join(parse_words(m)), alias_string())


ctx = Context("alias")
keymap = {
    "alias (start | record)": lambda m: macro.record(),
    "alias stop": alias_stop,
    "alias play": alias_play,
    "alias print": alias_print,
    "alias save [<dgndictation>]": alias_save,
}
keymap.update(_load_saved_macros())
ctx.keymap(keymap)

#
# def on_key(typ, e):
#     global last_macro
#     # we use e.up so the key isn't pressed while the macro is playing
#     if e.up:
#         if e == "f1":
#             e.block()
#             if not macro.recording:
#                 app.notify("Macro", "Recording.")
#                 macro.record()
#             else:
#                 last_macro = macro.finish()
#                 app.notify("Macro", "Recorded.")
#         elif e == "f2":
#             e.block()
#             # TODO: press f2 again to abort macro?
#             # TODO: lock or use cron to prevent overlapping execution?
#             if last_macro:
#                 app.notify("Macro", "Playing.")
#                 dispatch.async_call(lambda: macro.play(last_macro))
#                 app.notify("Macro", "Playback done.")
#         elif e == "f3":
#             e.block()
#             if last_macro:
#                 app.notify("Macro", "Playing (no delay).")
#                 dispatch.async_call(lambda: macro.play(last_macro, delay=False))
#                 app.notify("Macro", "Playback done.")
#     else:
#         if e == "f1" or e == "f2" or e == "f3":
#             e.block()
#
#
# tap.register(tap.KEY | tap.HOOK, on_key)
