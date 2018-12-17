import string
import collections
import itertools

from talon import clip
from talon.voice import Str, Key, press
from time import sleep

mapping = {
    "inc.": "incorporated",

    "yamel": "yaml",
    "semicolon": ";",
    "new-line": "\n",
    "new-paragraph": "\n\n",
    "teak": "k",
    "virg": "v",
    "zug": "s",
    "pre-": "pre",
    "in turn": "intern",
    "re- factor": "refactor",
    "re- factoring": "refactoring",
    "e-mail": "email",
    "fulsome": "folsom",
    "thumbs down": ":-1:",
    "thumbs-down": ":-1:",
    "thumbs up": ":+1:",
    "thumbs-up": ":+1:",
    "okay hand": ":ok_hand:",
    "thinking face": ":thinking_face:",
    "in-line": "in line",
    "jupiter": "jupyter",
    "pie": "py",
    ".pie": ".py",
    "dot pie": ".py",
    "dot by": ".py",
    "dot hi": ".py",
    ".hi": ".py",
    ". hi": ".py",
    ".by": ".py",
    "dot shell": ".sh",
    "self-taught": "self.",
    "self-doubt": "self.",
    "pip installed": "pip install",
    "rapper": "wrapper",
    "stack trace": "stacktrace",
    "repose": "repos",
    "ellis": "elif",
    "tubal": "tuple",
    "deck": "deque",
    "log it's": "logits",
    "sell": "cell",
    "jeep you": "gpu",
    "endo": "end",
    "and oh": "end",
    "rappers": "wrappers",
    "poynter": "pointer",
    "numb": "num",
    "gnome": "num",
    "don": "done",
    "jet": "git",
    "g cloud": "gcloud",
    "voice code": "voicecode",
    "nirvana": "nervana",
    "terrace": "keras",
    "karis": "keras",
    "me on": "neon",
    "cube nets": "kubernetes",
    "q burnett": "kubernetes",
    "cooper9": "kubernetes",
    "expand dimms": "expand dims",
    "dimms": "dims",
    "dems": "dims",
    "seek to seek": "Seq2Seq",
    "data set": "dataset",
    "data loader": "dataloader",
    "call back": "callback",
    "jim": "gym",
    "angie": "ng",
    "and g": "ng",
    "mg": "ng",
    "mp": "np",
    "and p": "np",
    "all the rhythms": "algorithms",
    "all rhythms": "algorithms",
    "waits": "weights",
    "wait": "weight",
    "dk": "decay",
    "epoque": "epoch",
    "epic": "epoch",
    "epoques": "epochs",
    "epics": "epochs",
    "1 hot": "onehot",
    "one hot": "onehot",
    "scaler": "scalar",
    "sql light": "sqlight",
    "post gress": "postgres",
    "sink": "sync",
    "and betting": "embedding",
    "I am betting": "embedding",
    "I'm betting": "embedding",
    "phil": "fill",
    "gam": "gan",
    "gann": "gan",
    "ncloud interactive": "ncloud interact",
    "adam": "atom",
    "pseudo-": "sudo",
    "pipe": "|",
    "apt get": "apt-get",
    "macron": "make run",
    "make show": "make shell",
    "standard out": "stdout",
    "standard in": "stdin",
    "standard error": "stderr",
    "les": "less",
    "doctor": "docker",
    "darker": "docker",
    "communities": "kubernetes",
    "shall": "shell",
    "w get": "wget",
    "backslash": "\\",
    "jet tub": "github",
    "git tub": "github",
    "jet hub": "github",
    "git hub": "github",
    "ron": "run",
    "thorpe": "\t",
    "tharp": "\t",

    # python
    "if not none": "if not None",
}
mappings = collections.defaultdict(dict)
for k, v in mapping.items():
    mappings[len(k.split(" "))][k] = v

punctuation = set(".,-!?")


def parse_word(word, force_lowercase=True):
    word = str(word).lstrip("\\").split("\\", 1)[0]
    if force_lowercase:
        word = word.lower()
    word = mapping.get(word, word)
    return word


def replace_words(words, mapping, count):
    if len(words) < count:
        return words

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


def parse_words(m, natural=False):
    if isinstance(m, list):
        words = m
    elif hasattr(m, 'dgndictation'):
        words = m.dgndictation[0]
    else:
        return []

    words = list(map(lambda current_word: parse_word(current_word, not natural), words))
    words = replace_words(words, mappings[2], 2)
    words = replace_words(words, mappings[3], 3)
    return words


def join_words(words, sep=" "):
    out = ""
    for i, word in enumerate(words):
        if i > 0 and word not in punctuation:
            out += sep
        out += str(word)
    return out


def insert(s):
    Str(s)(None)


def text(m):
    insert(join_words(parse_words(m)).lower())


def spoken_text(m):
    insert(join_words(parse_words(m, True)))


def sentence_text(m):
    raw_sentence = join_words(parse_words(m, True))
    sentence = raw_sentence[0].upper() + raw_sentence[1:]
    insert(sentence)


def word(m):
    try:
        text = join_words(list(map(parse_word, m.dgnwords[0]._words)))
        insert(text.lower())
    except AttributeError:
        pass


def surround(by):
    def func(i, word, last):
        if i == 0:
            word = by + word
        if last:
            word += by
        return word

    return func


def rot13(i, word, _):
    out = ""
    for c in word.lower():
        if c in string.ascii_lowercase:
            c = chr((((ord(c) - ord("a")) + 13) % 26) + ord("a"))
        out += c
    return out


numeral_map = dict((str(n), n) for n in range(0, 20))
for n in range(20, 101, 10):
    numeral_map[str(n)] = n
for n in range(100, 1001, 100):
    numeral_map[str(n)] = n
for n in range(1000, 10001, 1000):
    numeral_map[str(n)] = n
numeral_map["oh"] = 0  # synonym for zero
numeral_map["and"] = None  # drop me

numerals = " (" + " | ".join(sorted(numeral_map.keys())) + ")+"
optional_numerals = " (" + " | ".join(sorted(numeral_map.keys())) + ")*"


def text_to_number(words):
    tmp = [str(s).lower() for s in words]
    words = [parse_word(word) for word in tmp]

    result = 0
    factor = 1
    for word in reversed(words):
        print("{} {} {}".format(result, factor, word))
        if word not in numerals:
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


def m_to_number(m):
    tmp = [str(s).lower() for s in m._words]
    words = [parse_word(word) for word in tmp]

    result = 0
    factor = 1
    for word in reversed(words):
        if word not in numerals:
            # we consumed all the numbers and only the command name is left.
            break

        result = result + factor * int(numeral_map[word])
        factor = 10 * factor

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
        if not non_zero_found and n == '0':
            continue
        non_zero_found = True
        normalized_number_values.append(n)

    # If the entire sequence was zeros, return single zero
    if len(normalized_number_values) == 0:
        normalized_number_values = ['0']

    # Create merged number string and convert to int
    return int(''.join(normalized_number_values))

def alternatives(options):
    return " (" + " | ".join(sorted(options)) + ")+"


def select_single(options):
    return " (" + " | ".join(sorted(options)) + ")"


def optional(options):
    return " (" + " | ".join(sorted(options)) + ")*"


numeral_map = dict((str(n), n) for n in range(0, 20))
for n in [20, 30, 40, 50, 60, 70, 80, 90]:
    numeral_map[str(n)] = n
numeral_map["oh"] = 0  # synonym for zero

numerals = " (" + " | ".join(sorted(numeral_map.keys())) + ")+"
optional_numerals = " (" + " | ".join(sorted(numeral_map.keys())) + ")*"


def preserve_clipboard(fn):
    def wrapped_function(*args, **kwargs):
        old = clip.get()
        fn(*args, **kwargs)
        clip.set(old)

    return wrapped_function


# The. following function is used to be able to repeat commands by following it by one or several numbers, e.g.:
# 'delete' + optional_numerals: repeat_function(1, 'delete'),
def repeat_function(numberOfWordsBeforeNumber, keyCode, delay=0):
    def repeater(m):
        line_number = parse_words_as_integer(m._words[numberOfWordsBeforeNumber:])

        if line_number == None:
            line_number = 1

        for i in range(0, line_number):
            sleep(delay)
            press(keyCode)

    return repeater
