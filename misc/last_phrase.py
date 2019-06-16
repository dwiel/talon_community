import os

from atomicwrites import atomic_write
from talon import app, ui, webview
from talon.engine import engine
from talon.voice import Context
from talon_init import TALON_HOME

path = os.path.join(TALON_HOME, "last_phrase")
WEBVIEW = True
NOTIFY = False
hist_len = 6


def parse_phrase(phrase):
    return " ".join(word.split("\\")[0] for word in phrase)


def on_phrase(j):
    phrase = parse_phrase(j.get("phrase", []))
    cmd = j["cmd"]
    if cmd == "p.end" and phrase:
        with atomic_write(path, overwrite=True) as f:
            f.write(phrase)


engine.register("phrase", on_phrase)


template = """
<style type="text/css">
body {
    width: 400px;
    padding: 0;
    margin: 0;
}
.contents, table, h3 {
    width: 100%;
}
table {
    table-layout: fixed;
}
td {
    overflow-wrap: normal;
    word-wrap: normal;
    text-align: left;
    margin: 0;
    padding: 0;
    padding-left: 5px;
    padding-right: 5px;
}
.text {
    font-weight: normal;
    font-style: italic;
}
#title {
    padding-right: 5px; /* this is broken */
    min-width: 100px;
}
</style>

<h3 id="title">History</h3>
<table>
{% for phrase in phrases %}
<tr><td class="phrase">{{ phrase }}</td></tr>
{% endfor %}
<tr><td><i>{{ hypothesis }}</i></td></tr>
</ul>
"""

if WEBVIEW:
    webview = webview.Webview()
    webview.render(template, phrases=["command"])
    webview.show()
    webview.move(1, ui.main_screen().height)


class History:
    def __init__(self):
        self.visible = True
        self.history = []
        engine.register("post:phrase", self.on_phrase_post)

    def parse_phrase(self, phrase):
        return " ".join(word.split("\\")[0] for word in phrase)

    def on_phrase_post(self, j):
        phrase = self.parse_phrase(j.get("phrase", []))
        cmd = j["cmd"]
        if cmd == "p.end" and phrase:
            self.history.append(phrase)
            self.history = self.history[-hist_len:]
            if WEBVIEW:
                webview.render(template, phrases=self.history)
                self.refresh()
            if NOTIFY:
                app.notify(body="\r\n".join(self.history))

    def refresh(self):
        webview.hide()
        if self.visible:
            webview.show()

    def show(self):
        self.visible = True
        self.refresh()

    def hide(self):
        self.visible = False
        self.refresh()


history = History()

ctx = Context("last_phrase")
ctx.keymap(
    {
        "last phrase show": lambda m: history.show(),
        "last phrase hide": lambda m: history.hide(),
    }
)
