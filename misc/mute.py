"""
This script provides a quick way for disabling and re-enabling Talon.

The intended use cases include:

- Someone starts talking to you and you want to quickly disable the microphone
  to prevent random commands from being run
- You are working with someone, and so are switching between talking to them
  and dictating talon commands (e.g. by pair programming on your computer).

Notes:

- Due to this script using the same mechanism to disable the microphone as the
  misc/speech_toggle.py script, you can press and release the TRIGGER_KEY to
  enable the microphone rather than saying "Talon wake".
- At the moment, it does not disable the microphone in Dragon so if the
  microphone is awake, you must put it to sleep by saying "Go to sleep".
- There is a bug in Talon which means the microphone will not be re-enabled if
  you release the modifier keys before the main key in TRIGGER_KEY
  https://github.com/talonvoice/talon/issues/83 (this comment was added on
  Feburary 5, 2019)
"""

from talon import tap
from talon_plugins import speech
from talon import voice
from ..config import config

# Hold this key down to disable talon
TRIGGER_KEY = config.get("mute_trigger_key", "shift-ctrl-alt-a")


def on_key(typ, e):
    if e != TRIGGER_KEY:
        return

    e.block()

    should_be_enabled = e.up
    if voice.talon.enabled == should_be_enabled:
        return

    speech.set_enabled(should_be_enabled)


tap.register(tap.KEY | tap.HOOK, on_key)
