# originally from https://github.com/JonathanNickerson/talon_voice_user_scripts
# and https://github.com/pimentel/talon_user/blob/master/repeat.py
#
# based on the original voicecode spec https://voicecode.io/doc/repetition:
#   "hello repple two" types `hellohello`
#   "shock repple five" presses `return` key 5 times
#   "hello soup" is equivalent to "hello repple two"
#   "hello trace" is equivalent to "hello repple three"
#
#   Note, "hello repple one" or "hello wink" will also output hellohello, as in this case it
#   means 'repeat previous once more', whereas every parameter more than 1 means 'repeat previous N times in total'.
#
#   Creek repeats the entire previous phrase.
#   "hello world clamor trace" types "hello world!!!"
#   Then saying "shock creek" will type a newline followed by "hello world!!!" again

from talon.voice import Context, Rep, RepPhrase, talon
from .. import utils

ctx = Context("repeater")

# use this if you want `action trace` to result in action being executed 3 times
offset = -1
# use this if you want `action` pause `trace` to result in action being executed 4 times
# offset = 0


def repeat(m):
    # TODO: This could be made more intelligent:
    #         * Apply a timeout after which the command will not repeat previous actions
    #         * Prevent stacking of repetitions upon previous repetitions
    repeat_count = utils.extract_num_from_m(m)

    if repeat_count is not None:
        if repeat_count >= 2:
            repeat_count -= 1
        repeater = Rep(repeat_count)
        repeater.ctx = talon
        return repeater(None)


ctx.keymap(
    {
        "wink": Rep(1),
        "creek": RepPhrase(1),
        "soup": Rep(2 + offset),
        "trace": Rep(3 + offset),
        "quarr": Rep(4 + offset),
        "fypes": Rep(5 + offset),
        "(repeat | repple)" + utils.numerals: repeat,
    }
)
