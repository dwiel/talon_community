'''
This script provides a quick way for disabling and re-enabling Talon.

The intended use cases include:

- Someone starts talking to you and you want to quickly disable the microphone
  to prevent random commands from being run
- You are working with someone, and so are switching between talking to them
  and dictating talon commands (e.g. by pair programming on your computer).

Notes:

- At the moment, it does not disable the microphone in Dragon so if the
  microphone is awake, you must put it to sleep by saying "Go to sleep".
'''

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
