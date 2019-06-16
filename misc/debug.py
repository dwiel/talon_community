from talon.engine import engine
from talon import ui, voice, tap
import os

SAMPLE_DRAGON_KEY = "f1"

# Note: order of handlers matters
APPLIED_HANDLERS = (
    "catch_all",
    "hide_grammar",
    "abbr_listset",
    "ignore_successful_listset",
    "ignore_ui_event",
    "simplify_parse_result",
    "ignore_successful_reload",
    # "ignore_begin",
    # "ignore_empty",
    # "simplify",
)

handlers = {
    "catch_all": {"format": lambda m: m},
    "hide_grammar": {
        "event": ("g.load",),
        "cond": lambda m: m["success"] is True,
        "format": lambda m: m["cmd"].update({"data": "*hidden*"}) or m,
    },
    "abbr_listset": {
        "event": ("g.listset",),
        "cond": lambda m: "list" in m["cmd"],
        "format": lambda m: m["cmd"].update({"items": len(m["cmd"]["items"])}) or m,
    },
    "ignore_successful_listset": {
        "event": ("g.listset",),
        "cond": lambda m: m["success"] is True,
        "format": lambda m: "",
    },
    "ignore_successful_reload": {
        "event": ("g.unload", "g.load", "g.listset", "g.update"),
        "cond": lambda m: m["success"] is True,
        "format": lambda m: "",
    },
    "ignore_ui_event": {"topic": ("ui",), "format": lambda m: ""},
    "simplify_parse_result": {
        "event": ("p.end",),
        "cond": lambda m: "words" in m,
        "format": lambda m: {k: m[k] for k in m if k in ("cmd", "phrase", "parsed")},
    },
    "ignore_begin": {
        "event": ("p.begin",),
        "cond": lambda m: True,
        "format": lambda m: "",
    },
    "ignore_empty": {
        "event": ("p.end",),
        "cond": lambda m: m["phrase"] == [],
        "format": lambda m: "",
    },
    "simplify": {
        "event": ("p.end",),
        "cond": lambda m: "parsed" in m,
        "format": lambda m: f"{m['phrase']}: {m['parsed']._data}",
    },
}


def listener(topic, m):
    try:
        event = (
            m.get("cmd") if isinstance(m.get("cmd"), str) else m.get("cmd").get("cmd")
        )
    except (AttributeError):
        try:
            event = m.get("event")
        except (AttributeError):
            event = "unknown"

    new_m = None
    for handler in APPLIED_HANDLERS:
        h = handlers[handler]
        if "topic" not in h or topic in h["topic"]:
            if "event" not in h or event in h["event"]:
                if "cond" not in h or h["cond"](m):
                    new_m = h["format"](m)
    if new_m:
        print(topic, new_m)


engine.register("", listener)


def ui_event(event, arg):
    contexts = [ctx.name for ctx in voice.talon.active]
    listener(
        "ui",
        {"event": event, "arg": arg, "active": ui.active_app(), "contexts": contexts},
    ),


# sample dragon process to send to aegis for debugging
def on_key(typ, e):
    if e == SAMPLE_DRAGON_KEY:
        dragon = ui.apps(bundle="com.dragon.dictate")[0]
        os.popen(f"sample {dragon.pid} > /tmp/dragon.sample")
        e.block()


tap.register(tap.KEY | tap.HOOK, on_key)

# from talon import canvas, ui
#
# def draw(c):
#     rect = ui.active_window().rect
#     paint = c.paint
#     paint.style = paint.Style.STROKE
#     paint.color = 'ff0000'
#     c.draw_rect(rect)
#     # print('active rect', rect)
#
# canvas.register('overlay', draw)
