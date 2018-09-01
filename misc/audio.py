from talon.voice import Key, Context
from subprocess import Popen, PIPE

ctx = Context('audio')


def run_script(script):
    p = Popen(['osascript'], stdin=PIPE,
              stdout=PIPE, stderr=PIPE, universal_newlines=True)
    p.communicate(script)
    p.terminate()


def text_to_number(m, numwords={}):
    tmp = [str(s).lower() for s in m.dgndictation[0]._words]
    words = [parse_word(word) for word in tmp]

    # Special case to set volume to max
    if "hundred" in words:
        return 100

    if not numwords:
        units = [
            "zero", "one", "two", "three", "four", "five", "six",
            "seven", "eight", "nine", "ten", "eleven", "twelve",
            "thirteen", "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen"
        ]

        tens = [
            "", "", "twenty", "thirty", "forty", "fifty",
            "sixty", "seventy", "eighty", "ninety"
        ]

        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)

    result = 0
    for word in words:
        if word not in numwords:
            return -1

        scale, increment = numwords[word]
        result = result * scale + increment

    return result


def parse_word(word):
    word = word.lstrip('\\').split('\\', 1)[0]
    return word


def set_system_volume(m):
    volume = text_to_number(m)
    if volume == -1:
        return

    volume = str(volume)
    script = '''set volume output volume ''' + volume
    run_script(script)


keymap = {
    'volume <dgndictation>': set_system_volume,
}


ctx.keymap(keymap)
