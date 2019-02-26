import time

from talon.voice import Context, Key, press
from talon import clip
from .. import utils
from ..utils import is_in_bundles
from ..bundle_groups import BROWSER_BUNDLES

EMOJI_BUNDLES = (
    "com.tinyspeck.slackmacgap",
    #    *BROWSER_BUNDLES,
)

ctx = Context("emoji", func=is_in_bundles(EMOJI_BUNDLES))

emojis = {
    "thumbs up": ":+1:",
    "okay hand": ":ok_hand:",
    "okay": ":ok_hand:",
    "check": ":white_check_mark:",
    "crossed fingers": ":crossed_fingers:",
    "fingers": ":crossed_fingers:",
    "fingers": ":crossed_fingers:",
    "pray": ":pray:",
}


def react(m):
    key = utils.join_words(m._words[1:])
    emojis[key]

    old_clipboard = clip.get()

    try:
        press("cmd-a", wait=2000)
        time.sleep(0.25)
        press("cmd-c", wait=2000)
        time.sleep(0.25)
        old_text = clip.get()

        utils.insert("+" + emojis[key])
        press("enter", wait=2000)

        if old_clipboard != old_text:
            press("cmd-a", wait=2000)
            time.sleep(0.25)
            utils.insert(old_text)
    finally:
        clip.set(old_clipboard)


keymap = {
    "emo {}".format(name): representation for name, representation in emojis.items()
}
keymap.update(
    {
        "react {}".format(utils.select_single(emojis.keys())): react,
        # 'react {}'.format(name): ['+'+representation]
        # for name, representation in emojis.items()
    }
)


ctx.keymap(keymap)
