import os
import json

from talon import ui, resource
from talon.voice import Key, Context

from .. import utils


single_digits = "0123456789"
NAMED_DESKTOPS = {digit: int(digit) for digit in single_digits}
desktops_filename = utils.local_filename(__file__, "named_desktops.json")
NAMED_DESKTOPS.update(json.load(resource.open(desktops_filename)))

ctx = Context("spaces")

keymap = {}
keymap.update(
    {
        "desk %s" % name: Key("ctrl-%s" % NAMED_DESKTOPS[name])
        for name in NAMED_DESKTOPS.keys()
    }
)

keymap.update(
    {
        "window move desk %s" % name: Key("ctrl-alt-shift-%s" % NAMED_DESKTOPS[name])
        for name in NAMED_DESKTOPS.keys()
    }
)

ctx.keymap(keymap)
