import collections
import json
import os
from time import sleep

from talon import clip, resource
from talon.voice import Context, Str, press

from . import vocab
from .bundle_groups import FILETYPE_SENSITIVE_BUNDLES, TERMINAL_BUNDLES

VIM_IDENTIFIER = "(Vim)"
INCLUDE_TEENS_IN_NUMERALS = False
INCLUDE_TENS_IN_NUMERALS = False

# mapping = json.load(open(os.path.join(os.path.dirname(__file__), "replace_words.json")))
mapping = json.load(resource.open("replace_words.json"))
mapping.update({k.lower(): v for k, v in vocab.vocab_alternate.items()})
mappings = collections.defaultdict(dict)
for k, v in mapping.items():
    mappings[len(k.split(" "))][k] = v

punctuation = set(".,-!?/")


ordinal_indexes = {
    "first": 0,
    "second": 1,
    "third": 2,
    "fourth": 3,
    "fifth": 4,
    "sixth": 5,
    "seventh": 6,
    "eighth": 7,
    "ninth": 8,
    "tenth": 9,
    "final": -1,
    "next": "next",  # Yeah, yeah, not a number.
    "last": "last",
    "this": "this",
}


def local_filename(file, name):
    return os.path.join(os.path.dirname(os.path.realpath(file)), name)


def parse_word(word, force_lowercase=True):
    if force_lowercase:
        word = word.lower()
    word = mapping.get(word, word)

    return word


def replace_words(words, mapping, count):
    if len(words) < count:
        return words

    # print(words, mapping, count)

    new_words = []
    i = 0
    while i < len(words) - count + 1:
        phrase = words[i : i + count]
        key = " ".join(phrase)
        if key in mapping:
            new_words.append(mapping[key])
            i = i + count
        else:
            new_words.append(phrase[0])
            i = i + 1

    new_words.extend(words[i:])
    return new_words


def remove_dragon_junk(word):
    if word == ".\\point\\point":
        return "point"
    elif word == ".\\period\\period":
        return "period"
    else:
        return str(word).lstrip("\\").split("\\", 1)[0].replace("-", " ").strip()


def remove_appostrophe_s(words):
    if "'s" in words:
        new_words = []
        for i, word in enumerate(words):
            if word == "'s":
                new_words[-1] += "s"
            else:
                new_words.append(word)
        return new_words
    else:
        return words


def parse_words(m, natural=False):
    if isinstance(m, list):
        words = m
    elif hasattr(m, "dgndictation"):
        words = m.dgndictation[0]
    else:
        return []

    # split compound words like "pro forma" into two words.
    words = list(map(remove_dragon_junk, words))
    words = remove_appostrophe_s(words)
    words = sum([word.split(" ") for word in words], [])
    if not natural:
        words = [word.lower() for word in words]

    # replace words and all orders to make sure the replacement is more complete ... a more principled approach here would be nice
    words = replace_words(words, mappings[4], 4)
    words = replace_words(words, mappings[3], 3)
    words = replace_words(words, mappings[2], 2)
    words = replace_words(words, mappings[1], 1)
    # words = list(map(lambda current_word: parse_word(current_word, not natural), words))
    words = replace_words(words, mappings[2], 2)
    words = replace_words(words, mappings[3], 3)
    words = replace_words(words, mappings[4], 4)
    words = sum([word.split(" ") for word in words], [])

    return words


def join_words(words, sep=" "):
    out = ""
    for i, word in enumerate(words):
        if i > 0 and word not in punctuation and out[-1] not in ("/-"):
            out += sep
        out += str(word)
    return out


def insert(s):
    Str(s)(None)


def string_capture(m):
    return join_words(parse_words(m)).lower()


def text(m):
    insert(string_capture(m))


def snake_text(m):
    insert(join_words(parse_words(m), sep="_").lower())


def spoken_text(m):
    insert(join_words(parse_words(m, True)))


def sentence_text(m):
    raw_sentence = join_words(parse_words(m, True))
    sentence = raw_sentence[0].upper() + raw_sentence[1:]
    insert(sentence)


def word(m):
    try:
        text = join_words(
            map(lambda w: parse_word(remove_dragon_junk(w)), m.dgnwords[0]._words)
        )
        insert(text.lower())
    except AttributeError:
        pass


numeral_map = dict((str(n), n) for n in range(0, 10))
if INCLUDE_TEENS_IN_NUMERALS:
    for n in range(10, 20, 1):
        numeral_map[str(n)] = n
if INCLUDE_TENS_IN_NUMERALS:
    for n in range(20, 101, 10):
        numeral_map[str(n)] = n
for n in range(100, 1001, 100):
    numeral_map[str(n)] = n
for n in range(1000, 10001, 1000):
    numeral_map[str(n)] = n
numeral_map["oh"] = 0  # synonym for zero
numeral_map["and"] = None  # drop me

numeral_list = sorted(numeral_map.keys())

ctx = Context("n")
ctx.set_list("all", numeral_list)
numerals = " {n.all}+"
optional_numerals = " {n.all}*"


def text_to_number(words):
    tmp = [str(s).lower() for s in words]
    words = [parse_word(word) for word in tmp]

    result = 0
    factor = 1
    for word in reversed(words):
        if word not in numeral_list:
            raise Exception("not a number: {}".format(words))

        number = numeral_map[word]
        if number is None:
            continue

        number = int(number)
        if number > 10:
            result = result + number
        else:
            result = result + factor * number
        factor = (10 ** len(str(number))) * factor
    return result


def text_to_range(words, delimiter="until"):
    tmp = [str(s).lower() for s in words]
    split = tmp.index(delimiter)
    start = text_to_number(words[:split])
    end = text_to_number(words[split + 1 :])
    return start, end


number_conversions = {"oh": "0"}  # 'oh' => zero
for i, w in enumerate(
    ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
):
    number_conversions[str(i)] = str(i)
    number_conversions[w] = str(i)
    number_conversions["%s\\number" % (w)] = str(i)


def parse_words_as_integer(words):
    # TODO: Once implemented, use number input value rather than manually
    # parsing number words with this function

    # Ignore any potential non-number words
    number_words = [w for w in words if str(w) in number_conversions]

    # Somehow, no numbers were detected
    if len(number_words) == 0:
        return None

    # Map number words to simple number values
    number_values = list(map(lambda w: number_conversions[w.word], number_words))

    # Filter out initial zero values
    normalized_number_values = []
    non_zero_found = False
    for n in number_values:
        if not non_zero_found and n == "0":
            continue
        non_zero_found = True
        normalized_number_values.append(n)

    # If the entire sequence was zeros, return single zero
    if len(normalized_number_values) == 0:
        normalized_number_values = ["0"]

    # Create merged number string and convert to int
    return int("".join(normalized_number_values))


def alternatives(options):
    return " (" + " | ".join(sorted(map(str, options))) + ")+"


def select_single(options):
    return " (" + " | ".join(sorted(map(str, options))) + ")"


def optional(options):
    return " (" + " | ".join(sorted(map(str, options))) + ")*"


def preserve_clipboard(fn):
    def wrapped_function(*args, **kwargs):
        old = clip.get()
        ret = fn(*args, **kwargs)
        sleep(0.1)
        clip.set(old)
        return ret

    return wrapped_function


# @preserve_clipboard
def paste_text(text):
    with clip.revert():
        clip.set(text)
        # sleep(0.1)
        press("cmd-v")
        sleep(0.1)


# @preserve_clipboard
# def copy_selected():
#     press("cmd-c")
#     sleep(0.25)
#     return clip.get()


def copy_selected(default=None):
    try:
        with clip.capture() as s:
            press("cmd-c")
        return s.get()
    except clip.NoChange:
        return default


# The. following function is used to be able to repeat commands by following it by one or several numbers, e.g.:
# 'delete' + optional_numerals: repeat_function(1, 'delete'),
def repeat_function(numberOfWordsBeforeNumber, keyCode, delay=0):
    def repeater(m):
        line_number = parse_words_as_integer(m._words[numberOfWordsBeforeNumber:])

        if line_number is None:
            line_number = 1

        for i in range(0, line_number):
            sleep(delay)
            press(keyCode)

    return repeater


def delay(amount=0.1):
    return lambda _: sleep(amount)


def is_in_bundles(bundles):
    def _is_in_bundles(app, win):
        return any(b in app.bundle for b in bundles)

    return _is_in_bundles


def is_vim(app, win):
    if is_in_bundles(TERMINAL_BUNDLES)(app, win):
        if VIM_IDENTIFIER in win.title:
            return True
    return False


def is_not_vim(app, win):
    return not is_vim(app, win)


def is_filetype(extensions=(), default=False):
    def matcher(app, win):
        if is_in_bundles(FILETYPE_SENSITIVE_BUNDLES)(app, win):
            if any(ext in win.title for ext in extensions):
                return True
            else:
                return False
        return default

    return matcher


def extract_num_from_m(m, default=ValueError):
    # loop identifies numbers in any message
    number_words = [w for w in m._words if w in numeral_list]
    if len(number_words) == 0:
        if default is ValueError:
            raise ValueError("No number found")
        else:
            return default
    return text_to_number(number_words)


# Handle ( x | y ) syntax in dicts used to create keymaps indirectly.
# Do not be deceived, this is not real Talon syntax and [] wont work
def normalise_keys(dict):
    normalised_dict = {}
    for k, v in dict.items():
        for cmd in k.strip("() ").split("|"):
            normalised_dict[cmd.strip()] = v
    return normalised_dict
