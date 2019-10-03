from talon import app, clip, cron, resource
from talon.voice import Context, Str, press
from talon.webview import Webview
from ..misc.basic_keys import digits

from ..utils import parse_word
import os

########################################################################
# global settings
########################################################################

# a list of homophones where each line is a comma separated list
# e.g. where,wear,ware
# a suitable one can be found here:
# https://github.com/pimentel/homophones
cwd = os.path.dirname(os.path.realpath(__file__))
homophones_file = os.path.join(cwd, "homophones.csv")
# if quick_replace, then when a word is selected and only one homophone exists,
# replace it without bringing up the options
quick_replace = True
########################################################################

context = Context("homophones")
pick_context = Context("pick")

phones = {}
canonical = []
with resource.open(homophones_file, "r") as f:
    for h in f:
        h = h.rstrip()
        h = h.split(",")
        canonical.append(max(h, key=len))
        for w in h:
            w = w.lower()
            others = phones.get(w, None)
            if others is None:
                phones[w] = sorted(h)
            else:
                # if there are multiple hits, collapse them into one list
                others += h
                others = set(others)
                others = sorted(others)
                phones[w] = others

all_homophones = phones

active_word_list = None
is_selection = False

webview = Webview()
css_template = """
<style type="text/css">
body {
    padding: 0;
    margin: 0;
    font-size: 150%;
    min-width: 600px;
}

td {
    text-align: left;
    margin: 0;
    padding: 5px 10px;
}

h3 {
    padding: 5px 0px;
}

table {
    counter-reset: rowNumber;
}

table .count {
    counter-increment: rowNumber;
}

.count td:first-child::after {
    content: counter(rowNumber);
    min-with: 1em;
    margin-right: 0.5em;
}

.pick {
    font-weight: normal;
    font-style: italic;
}

.cancel {
    text-align: center;
}

</style>
"""

phones_template = (
    css_template
    + """
<div class="contents">
<h3>homophones</h3>
<table>
{% for word in homophones %}
<tr class="count"><td class="pick">🔊 pick </td><td>{{ transform(word) }}</td></tr>
{% endfor %}
<tr><td colspan="2" class="pick cancel">🔊 cancel</td></tr>
</table>
</div>
"""
)


def close_homophones():
    webview.hide()
    pick_context.unload()


def make_selection(m, is_selection, transform=lambda x: x):
    cron.after("0s", close_homophones)
    words = m._words
    d = None
    if len(words) == 1:
        d = int(parse_word(words[0]))
    else:
        d = int(parse_word(words[1]))
    w = active_word_list[d - 1]
    if len(words) > 1:
        w = transform(w)
    insert(w, is_selection)


def insert(w, is_selection):
    if is_selection:
        clip.set(w)
        press("cmd-v", wait=0)
    else:
        Str(w)(None)


def get_selection():
    with clip.capture() as s:
        press("cmd-c", wait=0)
    return s.get()


def capitalize(x):
    return x[0].upper() + x[1:]


def uppercase(x):
    return x.upper()


def lowercase(x):
    return x.lower()


def raise_homophones(m, force_raise=False, is_selection=False):
    global pick_context
    global active_word_list

    if is_selection:
        word = get_selection()
        word = word.strip()
        digit = int(digits[m._words[1]]) if len(m._words) == 2 else None

    # elif hasattr(m, "dgndictation"):
    #     # this mode is currently disabled...
    #     # experimenting with using a canonical representation and not using
    #     # dgndictation
    #     word = str(m.dgndictation[0]._words[0])
    #     word = parse_word(word)
    else:
        digit = int(digits[m._words[1]]) if str(m._words[1]) in digits else None
        word = parse_word(m._words[(2 if digit else 1)])

    if word == word.capitalize():
        transformer = capitalize
    elif word.isupper():
        transformer = uppercase
    else:
        transformer = lowercase

    word = word.lower()

    if word not in all_homophones:
        app.notify("homophones.py", '"%s" not in homophones list' % word)
        return

    active_word_list = all_homophones[word]
    if quick_replace and not force_raise:
        if not digit and len(active_word_list) == 2:
            if word == active_word_list[0].lower():
                new = active_word_list[1]
            else:
                new = active_word_list[0]
            return insert(transformer(new), is_selection)
        elif digit:
            new = active_word_list[digit - 1]
            return insert(new, is_selection)

    valid_indices = range(len(active_word_list))

    webview.render(phones_template, homophones=active_word_list, transform=transformer)
    webview.show()

    keymap = {"(cancel | 0)": lambda x: close_homophones()}

    keymap.update(
        {
            "[pick] %s"
            % (i + 1): lambda m: make_selection(m, is_selection, transformer)
            for i in valid_indices
        }
    )
    keymap.update(
        {
            "(ship | title) %s"
            % (i + 1): lambda m: make_selection(m, is_selection, capitalize)
            for i in valid_indices
        }
    )
    keymap.update(
        {
            "(yeller | upper | uppercase) %s"
            % (i + 1): lambda m: make_selection(m, is_selection, uppercase)
            for i in valid_indices
        }
    )
    keymap.update(
        {
            "(lower | lowercase) %s"
            % (i + 1): lambda m: make_selection(m, is_selection, lowercase)
            for i in valid_indices
        }
    )
    pick_context.keymap(keymap)
    pick_context.load()


help_template = (
    css_template
    + """
<div class="contents">
<h3>homophones help</h3>
<table>
<tr><td class="pick">🔊 phones</td><td>look up homophones for selected text</td></tr>
<tr><td class="pick">🔊 phones [word]</td><td>look up homophones for a given word</td></tr>
<tr><td class="pick">🔊 pick [number]</td><td>make a selection from the homophone list</td></tr>
<tr><td class="pick">🔊 ship [number]</td><td>make a selection and capitalize it</td></tr>
<tr><td class="pick">🔊 yeller [number]</td><td>make a selection and uppercase it</td></tr>
<tr><td class="pick">🔊 lower [number]</td><td>make a selection and lowercase it</td></tr>
<tr><td colspan="2" class="pick cancel">🔊 cancel</td></tr>
</table>
</div>
"""
)


def homophones_help(m):
    webview.render(help_template)
    webview.show()

    keymap = {"(cancel | exit)": lambda x: close_homophones()}
    pick_context.keymap(keymap)
    pick_context.load()


context.keymap(
    {
        "phones help": homophones_help,
        "phones {basic_keys.digits}* {homophones.canonical}": raise_homophones,
        "phones {basic_keys.digits}*": lambda m: raise_homophones(m, is_selection=True),
        "force phones {homophones.canonical}": lambda m: raise_homophones(
            m, force_raise=True
        ),
        "force phones": lambda m: raise_homophones(
            m, force_raise=True, is_selection=True
        ),
    }
)
context.set_list("canonical", canonical)
