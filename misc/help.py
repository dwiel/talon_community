import string
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


def on_click(data):
    if data["id"] == "cancel":
        return close_webview()
    elif "page" in data["id"]:
        context, _, page = data["id"].split("-")
        if context == "contexts":
            return render_contexts_help(_, int(page))
        return render_commands_webview(get_context(context), int(page))
    else:
        return render_commands_webview(voice.talon.subs.get(data["id"]))


webview = Webview()
webview.register("click", on_click)

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

    .cancel {
        text-align: center;
    }

    .pick {
        font-weight: normal;
        font-style: italic;
    }

    .item:hover {
        background-color: #858e96;
        color: white;
        cursor: pointer;
    }

    tr.inactive {
        color: #858e96;
    }

    td {
        text-align: left;
        margin: 0;
        padding: 0;
        padding-left: 5px;
        width: 1px;
        white-space: nowrap;
    }

    button {
        padding: 0;
        border: none;
        background: none;
        color: white;
        font-size: """
    + str(round(FONT_SIZE * 0.8))
    + """px;
    }
</style>
"""
)

templates = {
    "alpha": css_template
    + """
    <h3>alphabet</h3>
    <div class="contents">
    <table>
    {% for word, letter in kwargs['alphabet'] %}
        <tr><td>{{ letter }}</td><td>{{ word }}</td></tr>
    {% endfor %}
    <tr id="cancel" class="item events event-click"><td colspan="2" class="pick cancel">🔊 cancel</td></tr>
    </table>
    </div>
    """,
    "commands": css_template
    + """
    <h3>
    {% if kwargs['current_page'] | int > 1 %}
        <button type="button" style="float: left" class="item events event-click" id="{{ kwargs['context_name'] }}-page-{{ kwargs['current_page'] | int - 1 }}">prev</button>
    {% endif %}
    {{ kwargs['context_name'] }} commands
    {% if kwargs['total_pages'] | int > 1 %}
        <small> - page {{ kwargs['current_page'] }} of {{ kwargs['total_pages'] }}</small>
    {% endif %}
    {% if kwargs['current_page'] | int < kwargs['total_pages'] %}
        <button type="button" style="float: right" class="item events event-click" id="{{ kwargs['context_name'] }}-page-{{ kwargs['current_page'] | int + 1 }}">next</button>
    {% endif %}
    </h3>
    <div class="contents" overflow=scroll max-height=8px>
    <table>
    {% for trigger, mapped_to in kwargs['mapping'] %}
        <tr><td class="pick">🔊 {{ trigger }}</td><td>{{ mapped_to|e }}</td></tr>
    {% endfor %}
    <tr id="cancel" class="item events event-click"><td colspan="2" class="pick cancel">🔊 cancel</td></tr>
    </table>
    </div>
    """,
    "contexts": css_template
    + """
    <h3>
    {% if kwargs['current_page'] | int > 1 %}
        <button type="button" style="float: left" class="item events event-click" id="contexts-page-{{ kwargs['current_page'] | int - 1 }}"><</button>
    {% endif %}
    contexts
    {% if kwargs['total_pages'] | int > 1 %}
    <small> - {{ kwargs['current_page'] }} of {{ kwargs['total_pages'] }}</small>
    {% endif %}
    {% if kwargs['current_page'] | int < kwargs['total_pages'] %}
        <button type="button" style="float: right" class="item events event-click" id="contexts-page-{{ kwargs['current_page'] | int + 1 }}">></button>
    {% endif %}
    </h3>
    <div class="contents">
    <table>
    {% for index, context in kwargs['contexts'] %}
    <tr id="{{ context.name }}" class="item events event-click{% if context not in kwargs['actives'] %} inactive{% endif %}">
        <td class="pick">🔊 help {{ index }}</td><td>{{ context.name }}</td>
    </tr>
    {% endfor %}
    <tr id="cancel" class="item events event-click"><td colspan="2" class="pick cancel">🔊 cancel</td></tr>
    </table>
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


def render_alphabet_help(_):
    alphabet = list(zip(basic_keys.alpha_alt, string.ascii_lowercase))
    render_webview(templates["alpha"], {}, alphabet=alphabet)


# needed because of how closures work in Python
def create_context_mapping(context):
    return lambda _: render_commands_webview(context)


def render_contexts_help(_, target_page=1):
    contexts = []
    keymap = {}

    for idx, context in enumerate(voice.talon.subs.values()):
        contexts.append((idx + 1, context))
        keymap.update({"help " + str(idx + 1): create_context_mapping(context)})

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
        contexts=pages[target_page - 1],
        actives=voice.talon.active,
        current_page=target_page,
        total_pages=len(pages),
    )


# alternatives handle edge cases:
# - commonly misheard contexts
# - context names that are homophones
# - alternative pronunciations for convenience

# To add an alternative, add the preferred voice command as the key, and the
# context name as defined in the module as the value
alternatives = {
    "pearl": "perl",
    "icontrol": "eye_control",
    "lack": "slack",
    "chrome": "GoogleChrome",
    "get": "git",
    "docs": "googledocs",
    "google docs": "googledocs",
    "see": "c",
    "adam": "atom",
}


def clean_word(word):
    # removes some extra stuff added by dragon, e.g. 'I\\pronoun'
    return str(word).split("\\", 1)[0]


def normalize_words(words):
    words = [clean_word(w) for w in words]
    return "".join(words).lower().replace(" ", "")


def normalize_context(context):
    return context.replace("_", "").lower()


def contexts():
    contexts = {normalize_context(k): v for k, v in voice.talon.subs.items()}

    for k, v in alternatives.items():
        if v in contexts:
            contexts[k] = contexts[v]
    return contexts


def get_context(context_name):
    return contexts().get(normalize_words(context_name))


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
    return ", ".join([format_action(a) for a in actions])


def render_commands_help(m):
    context = get_context(m["help.contexts"])
    if not context:
        return

    return render_commands_webview(context)


def render_commands_webview(context, target_page=1):

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
        mapping=(pages[target_page - 1] if pages else []),
        current_page=target_page,
        total_pages=len(pages),
    )


keymap = {
    "help alphabet": render_alphabet_help,
    "help [commands] {help.contexts}": render_commands_help,
    "help context": render_contexts_help,
}
ctx.set_list("contexts", contexts().keys())
ctx.keymap(keymap)
