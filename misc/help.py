import string
from collections import OrderedDict
import talon
from talon import voice, ui
from talon.voice import Context, Key
from talon.webview import Webview
from . import basic_keys


# reusable constant for font size (in pixels), to use in calculations
FONT_SIZE = 12
# border spacing, in pixels
BORDER_SIZE = 2

main = ui.main_screen().visible_rect
# need to account for header and footer / pagination links, hence '-2'
MAX_ITEMS = int(main.height // (FONT_SIZE + 2 * BORDER_SIZE) - 2)

ctx = Context("help")
webview_context = Context("web_view")

webview = Webview()

css_template = (
    """
<style type="text/css">
    body {
        padding: 0;
        margin: 0;
        font-size: """
    + str(FONT_SIZE)
    + """px;
        -webkit-border-vertical-spacing: """
    + str(BORDER_SIZE)
    + """px;
        -webkit-border-horizontal-spacing: """
    + str(BORDER_SIZE)
    + """px;
    }

    .contents {
        width: 100%;
    }

    td {
        text-align: left;
        margin: 0;
        padding: 0;
        padding-left: 5px;
        width: 1px;
        white-space: nowrap;
    }

    footer {
        background-color: #696969;
        color: white;
        font-weight: bold;
    }
</style>
"""
)

# TODO: use a master template
templates = {
    "alpha": css_template
    + """
    <h3>alphabet</h3>
    <div class="contents">
    <table>
    {% for word, letter in alphabet %}
        <tr><td>{{ letter }}</td><td>{{ word }}</td></tr>
    {% endfor %}
    </table>
    </div>
    """,
    "commands": css_template
    + """
    <h3>{{ context_name }} commands</h3>
    <div class="contents" overflow=scroll max-height=8px>
    <table>
    {% for trigger, mapped_to in mapping %}
        <tr><td>{{ trigger }}</td><td>{{ mapped_to|e }}</td></tr>
    {% endfor %}
    </table>
    <footer>
    {% if current_page %}
        page {{ current_page }} of {{ total_pages }}
    {% endif %}
    </footer>
    </div>
    """,
    "contexts": css_template
    + """
    <h3>contexts</h3>
    <div class="contents">
    <table>
    {% for index, context in contexts.items() %}
        <tr>
            <td>{{ index }}</td><td>{{ context.name }}</td>
            <td>{% if context in actives %}✅{% else %}❌{% endif %} </td>
        </tr>
    {% endfor %}
    </table>
    </div>
    """,
}


def show_alphabet(_):
    alphabet = list(zip(basic_keys.alpha_alt, string.ascii_lowercase))

    webview_context.keymap({"(0 | quit | exit | escape)": lambda x: close_webview()})
    webview_context.load()

    webview.render(templates["alpha"], alphabet=alphabet)
    webview.show()


def close_webview():
    webview.hide()
    webview_context.unload()


# needed because of how closures work in Python
def create_context_mapping(context):
    return lambda _: show_commands(context)


def show_contexts(_):
    contexts = OrderedDict()

    keymap = {"(0 | quit | exit | escape)": lambda x: close_webview()}

    # grab all contexts and bind each to numbers (only for the webview)
    for idx, context in enumerate(voice.talon.subs.values()):
        contexts[idx + 1] = context
        keymap.update({str(idx + 1): create_context_mapping(context)})

    webview_context.keymap(keymap)
    webview_context.load()

    webview.render(templates["contexts"], contexts=contexts, actives=voice.talon.active)
    webview.show()


mapping = {
    "pearl": "perl",
    "i term": "iterm",
    "lack": "slack",
    "chrome": "googlechrome",
    "get": "git",
    "docs": "googledocs",
    "google docs": "googledocs",
}


def clean_word(word):
    # removes some extra stuff added by dragon, e.g. 'I\\pronoun'
    return str(word).split("\\", 1)[0]


def find_and_show(m):
    words = [clean_word(w) for w in m.dgndictation[0]._words]

    find = "".join(words).lower().replace(" ", "")
    find = mapping.get(find, find)

    contexts = {k.lower(): v for k, v in voice.talon.subs.items()}

    if find in contexts:
        show_commands(contexts[find])
        return

        # maybe context name is snake case
    find = "_".join(words).lower()
    if find in contexts:
        show_commands(contexts[find])


def format_action(action):
    actions = action if isinstance(action, (list, tuple)) else [action]

    pretty = []
    for action in actions:
        if isinstance(action, talon.voice.Key):
            keys = action.data.split(" ")
            if len(keys) > 1 and len(set(keys)) == 1:
                pretty.append(f"key({keys[0]}) * {len(keys)}")
            else:
                pretty.append(f"key({action.data})")
        elif isinstance(action, talon.voice.Str):
            pretty.append(f'"{action.data}"')
        elif isinstance(action, talon.voice.Rep):
            pretty.append(f'"{action.data}"')
        elif isinstance(action, voice.RepPhrase):
            pretty.append(f"repeat_phrase({action.data})")
        elif isinstance(action, str):
            pretty.append(f'"{action}"')
        elif callable(action):
            pretty.append(f"{action.__name__}()")
        else:
            pretty.append(str(action))

    if len(pretty) == 1:
        pretty = pretty[0]

    return pretty


def render_page(context, mapping, current_page, total_pages):
    webview.render(
        templates["commands"],
        context_name=context.name,
        mapping=mapping,
        current_page=current_page,
        total_pages=total_pages,
    )


def create_render_page(context, items, current_page, total_pages):
    return lambda _: render_page(context, items, current_page, total_pages)


def show_commands(context):
    # what you say is stored as a trigger
    mapping = []
    for trigger in context.triggers.keys():
        action = context.mapping[context.triggers[trigger]]
        mapping.append((trigger, format_action(action)))

    keymap = {
        "(0 | quit | exit | escape)": lambda x: close_webview(),
        "up": Key("pgup"),
        "down": Key("pgdown"),
    }

    total_pages = int(len(mapping) // MAX_ITEMS)
    if len(mapping) % MAX_ITEMS > 0:
        total_pages += 1

    pages = []

    # add elements to each page based on the page index
    for page in range(1, total_pages + 1):
        pages.append(mapping[((page - 1) * MAX_ITEMS) : (page * MAX_ITEMS)])

        # create the commands to navigate through pages
    for idx, items in enumerate(pages):
        page = idx + 1
        keymap.update(
            {"page " + str(page): create_render_page(context, items, page, total_pages)}
        )

    render_page(context, pages[0], 1, total_pages)

    webview_context.keymap(keymap)
    webview_context.load()
    webview.show()


keymap = {
    "help alphabet": show_alphabet,
    "help [commands] <dgndictation>": find_and_show,
    "help context": show_contexts,
}

ctx.keymap(keymap)
