import time

from .. import utils
from talon.voice import Context, Key

ctx = Context("sleep")


def sleep(m):
    seconds = extract_num_from_m(m, default=None)
    time.sleep(seconds)


ctx.keymap({"sleep" + utils.numerals: sleep})
