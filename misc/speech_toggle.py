from talon.voice import Context, ContextGroup
from talon.engine import engine
from talon_plugins import speech

sleep_group = ContextGroup('sleepy')
sleepy = Context('sleepy', group=sleep_group)

dictation_group = ContextGroup('dictation')
dictation = Context('dictation', group=dictation_group)
dictation_group.load()
dictation_group.disable()

sleepy.keymap({
    'talon sleep': lambda m: speech.set_enabled(False),
    'talon wake': lambda m: speech.set_enabled(True),

    'dragon mode': [lambda m: speech.set_enabled(False), lambda m: dictation_group.disable(), lambda m: engine.mimic('wake up'.split())],
    'dictation mode': [lambda m: speech.set_enabled(False), lambda m: engine.mimic('go to sleep'.split()), lambda m: dictation_group.enable()],
    'talon mode': [lambda m: speech.set_enabled(True), lambda m: dictation_group.disable(), lambda m: engine.mimic('go to sleep'.split())],
    'full sleep mode': [lambda m: speech.set_enabled(False), lambda m: dictation_group.disable(), lambda m: engine.mimic('go to sleep'.split())]
})
sleep_group.load()
