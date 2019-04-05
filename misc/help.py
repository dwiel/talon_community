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
BORDER_SIZE = int(FONT_SIZE / 6)

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
    {% for word, letter in kwargs['alphabet'] %}
        <tr><td>{{ letter }}</td><td>{{ word }}</td></tr>
    {% endfor %}
    </table>
    </div>
    """,
    "commands": css_template
    + """
    <h3>{{ kwargs['context_name'] }} commands</h3>
    <div class="contents" overflow=scroll max-height=8px>
    <table>
    {% for trigger, mapped_to in kwargs['mapping'] %}
        <tr><td>{{ trigger }}</td><td>{{ mapped_to|e }}</td></tr>
    {% endfor %}
    </table>
    <footer>
    {% if kwargs['current_page'] %}
        page {{ kwargs['current_page'] }} of {{ kwargs['total_pages'] }}
    {% endif %}
    </footer>
    </div>
    """,
    "contexts": css_template
    + """
    <h3>contexts</h3>
    <div class="contents">
    <table>
    {% for index, context in kwargs['contexts'] %}
        <tr>
            <td>{{ index }}</td><td>{{ context.name }}</td>
            <td>{% if context in kwargs['actives'] %}✅{% else %}❌{% endif %} </td>
        </tr>
    {% endfor %}
    </table>
    <footer>
    {% if kwargs['current_page'] %}
        page {{ kwargs['current_page'] }} of {{ kwargs['total_pages'] }}
    {% endif %}
    </footer>
    </div>
    """,
}


def render_page(template, **kwargs):
    webview.render(template, kwargs=kwargs)


def create_render_page(template, **kwargs):
    return lambda _: render_page(template, **kwargs)


def build_pages(items):
    total_pages = int(len(items) // MAX_ITEMS)
    if len(items) % MAX_ITEMS > 0:
        total_pages += 1

    pages = []

    # add elements to each page based on the page index
    for page in range(1, total_pages + 1):
        pages.append(items[((page - 1) * MAX_ITEMS) : (page * MAX_ITEMS)])

    return pages


def render_webview(template, keymap, **kwargs):
    keymap.update({"cancel": lambda x: close_webview()})
    webview_context.keymap(keymap)
    webview_context.load()
    render_page(template, **kwargs)
    webview.show()


def close_webview():
    webview.hide()
    webview_context.unload()


def show_alphabet(_):
    alphabet = list(zip(basic_keys.alpha_alt, string.ascii_lowercase))
    render_webview(templates["alpha"], {}, alphabet=alphabet)


# needed because of how closures work in Python
def create_context_mapping(context):
    return lambda _: show_commands(context)


def show_contexts(_):
    contexts = []
    keymap = {}

    for idx, context in enumerate(voice.talon.subs.values()):
        contexts.append((idx + 1, context))
        keymap.update({"show " + str(idx + 1): create_context_mapping(context)})

    pages = build_pages(contexts)

    for idx, items in enumerate(pages):
        keymap.update(
            {
                "page "
                + str(idx + 1): create_render_page(
                    templates["contexts"],
                    contexts=items,
                    actives=voice.talon.active,
                    current_page=idx + 1,
                    total_pages=len(pages),
                )
            }
        )

    render_webview(
        templates["contexts"],
        keymap,
        contexts=pages[0],
        actives=voice.talon.active,
        current_page=1,
        total_pages=len(pages),
    )


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
    if isinstance(action, talon.voice.Key):
        keys = action.data.split(" ")
        if len(keys) > 1 and len(set(keys)) == 1:
            return f"key({keys[0]}) * {len(keys)}"
        else:
            return f"key({action.data})"
    elif isinstance(action, talon.voice.Str):
        return f'"{action.data}"'
    elif isinstance(action, talon.voice.Rep):
        return f'"{action.data}"'
    elif isinstance(action, voice.RepPhrase):
        return f"repeat_phrase({action.data})"
    elif isinstance(action, str):
        return f'"{action}"'
    elif callable(action):
        return f"{action.__name__}()"
    else:
        return str(action)


def format_actions(actions):
    actions = actions if isinstance(actions, (list, tuple)) else [actions]
    return [format_action(a) for a in actions]


def show_commands(context):
    # what you say is stored as a trigger
    mapping = []
    for trigger in context.triggers.keys():
        actions = context.mapping[context.triggers[trigger]]
        mapping.append((trigger, format_actions(actions)))

    pages = build_pages(mapping)
    keymap = {}

    # create the commands to navigate through pages
    for idx, items in enumerate(pages):
        keymap.update(
            {
                "page "
                + str(idx + 1): create_render_page(
                    templates["commands"],
                    context_name=context.name,
                    mapping=items,
                    current_page=idx + 1,
                    total_pages=len(pages),
                )
            }
        )

    render_webview(
        templates["commands"],
        keymap,
        context_name=context.name,
        mapping=(pages[0] if pages else []),
        current_page=1,
        total_pages=len(pages),
    )


keymap = {
    "help alphabet": show_alphabet,
    "help [commands] <dgndictation>": find_and_show,
    "help context": show_contexts,
}

ctx.keymap(keymap)
