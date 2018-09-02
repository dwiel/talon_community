from talon.api import lib
from talon.voice import Context, ContextGroup, talon
from talon.engine import engine
from talon import app

def set_enabled(enable):
    if enable:
        talon.enable()
        app.icon_color(0, 0.7, 0, 1)
    else:
        talon.disable()
        app.icon_color(1, 0, 0, 1)
    lib.menu_check(b'!Enable Speech Recognition', enable)

def on_menu(item):
    if item == '!Enable Speech Recognition':
        set_enabled(not talon.enabled)

app.register('menu', on_menu)
set_enabled(talon.enabled)

sleep_group = ContextGroup('sleepy')
sleepy = Context('sleepy', group=sleep_group)

sleepy.keymap({
    'talon sleep': lambda m: set_enabled(False),
    'talon wake': lambda m: set_enabled(True),

    'dragon mode': [lambda m: set_enabled(False), lambda m: engine.mimic('wake up'.split())],
    'talon mode': [lambda m: set_enabled(True), lambda m: engine.mimic('go to sleep'.split())],
})
sleep_group.load()
