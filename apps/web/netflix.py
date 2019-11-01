from talon.voice import Context

from . import browser
from ...misc import audio

context = Context(
    "netflix", func=browser.url_matches_func("https://www.netflix.com/.*")
)
context.keymap(
    {"full screen": [lambda m: audio.set_volume(100), browser.send_to_page("f")]}
)
