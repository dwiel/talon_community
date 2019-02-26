from talon.engine import engine
from talon import ui, voice

CRAZY = False
VERBOSE = True
UI_EVENTS = False


def listener(topic, m):
    if topic == "cmd" and m["cmd"]["cmd"] == "g.load" and m["success"] == True:
        print("[grammar reloaded]")
    elif topic == "cmd" and m["cmd"]["cmd"] == "g.listset" and "list" in m["cmd"]:
        m["cmd"]["items"] = len(m["cmd"]["items"])
        print("here", topic, m)
    else:
        if CRAZY:
            print(topic, m)
        elif VERBOSE and topic == "cmd" and m["cmd"]["cmd"] != "g.listset":
            print(topic, m)
        elif topic == "phrase" and "words" in m and m["cmd"] != "p.hypothesis":
            try:
                print(topic, m["phrase"], m["parsed"])
            except:
                print(topic, m)


engine.register("", listener)


def ui_event(event, arg):
    contexts = [ctx.name for ctx in voice.talon.active]
    print(
        "ui_event",
        {"event": event, "arg": arg, "active": ui.active_app(), "contexts": contexts},
    )


if UI_EVENTS:
    ui.register("", ui_event)
