import os

from talon.voice import Word, Context, Key, Rep, RepPhrase, Str, press
from talon import ctrl, clip
from talon_init import TALON_HOME, TALON_PLUGINS, TALON_USER

from ..utils import parse_word, surround, text, sentence_text, word, parse_words, spoken_text


def title_case_capitalize_word(index, word, _):
    words_to_keep_lowercase = (
        'a,an,the,at,by,for,in,of,on,to,up,and,as,but,or,nor'.split(',')
    )
    if index == 0 or word not in words_to_keep_lowercase:
        return word.capitalize()
    else:
        return word


formatters = {
    "cram": (True, lambda i, word, _: word if i == 0 else word.capitalize()),
    "pathway": (True, lambda i, word, _: word if i == 0 else "/" + word),
    "dotsway": (True, lambda i, word, _: word if i == 0 else "." + word),
    "yellsmash": (True, lambda i, word, _: word.upper()),
    "yellsnik": (
        True,
        lambda i, word, _: word.upper() if i == 0 else "_" + word.upper(),
    ),
    "dollcram": (True, lambda i, word, _: "$" + word if i == 0 else word.capitalize()),
    "champ": (True, lambda i, word, _: word.capitalize() if i == 0 else " " + word),
    "lowcram": (True, lambda i, word, _: "@" + word if i == 0 else word.capitalize()),
    "criff": (True, lambda i, word, _: word.capitalize()),
    "criffed": (True, lambda i, word, _: word.capitalize()),
    "yeller": (False, lambda i, word, _: word.upper()),
    "dunder": (True, lambda i, word, _: "__%s__" % word if i == 0 else word),
    "camel": (True, lambda i, word, _: word if i == 0 else word.capitalize()),
    "snake": (True, lambda i, word, _: word if i == 0 else "_" + word),
    "dot": (True, lambda i, word, _: "." + word if i == 0 else "_" + word),
    "smash": (True, lambda i, word, _: word),
    # spinal or kebab?
    "spine": (True, lambda i, word, _: word if i == 0 else "-" + word),
    # 'sentence':  (False, lambda i, word, _: word.capitalize() if i == 0 else word),
    "title": (False, title_case_capitalize_word),
    "tridal": (False, lambda i, word, _: word.capitalize()),
    "allcaps": (False, lambda i, word, _: word.upper()),
    "dubstring": (False, surround('"')),
    "coif": (False, surround('"')),
    "string": (False, surround("'")),
    "posh": (False, surround("'")),
    "tics": (False, surround("`")),
    "padded": (False, surround(" ")),
}


def FormatText(m):
    fmt = []
    for w in m._words:
        if isinstance(w, Word) and w != "over":
            fmt.append(w.word)
    words = parse_words(m)
    if not words:
        with clip.capture() as s:
            press("cmd-c")
        words = s.get().split(" ")
        if not words:
            return

    tmp = []
    spaces = True
    for i, word in enumerate(words):
        word = parse_word(word).lower()
        for name in reversed(fmt):
            smash, func = formatters[name]
            word = func(i, word, i == len(words) - 1)
            spaces = spaces and not smash
        tmp.append(word)
    words = tmp

    sep = " "
    if not spaces:
        sep = ""
    Str(sep.join(words))(None)


ctx = Context("formatters")

ctx.keymap({
    "phrase <dgndictation> [over]": text,
    "sentence <dgndictation> [over]": sentence_text,
    "comma <dgndictation> [over]": [", ", spoken_text],
    "period <dgndictation> [over]": [". ", sentence_text],
    "word <dgnwords>": word,
    "(%s)+ <dgndictation> [over]" % (" | ".join(formatters)): FormatText,
})
