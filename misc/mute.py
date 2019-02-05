from talon import tap
from talon_plugins import speech
from talon import voice

# Hold this key down to disable talon
TRIGGER_KEY = 'shift-ctrl-a'


def on_key(typ, e):
    if e != TRIGGER_KEY:
        return

    e.block()

    should_be_enabled = e.up
    if voice.talon.enabled == should_be_enabled:
        return

    speech.set_enabled(should_be_enabled)


tap.register(tap.KEY | tap.HOOK, on_key)
