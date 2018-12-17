import os
from atomicwrites import atomic_write

from talon import app, webview
from talon.engine import engine
from talon_init import TALON_HOME

path = os.path.join(TALON_HOME, 'last_phrase')
WEBVIEW = False
NOTIFY = True

if WEBVIEW:
    webview = webview.Webview()
    webview.body = '<i>[waiting&nbsp;for&nbsp;phrase]</i>'
    webview.show()

def parse_phrase(phrase):
    return ' '.join(word.split('\\')[0] for word in phrase)

def on_phrase(j):
    phrase = parse_phrase(j.get('phrase', []))
    cmd = j['cmd']
    if cmd == 'p.end' and phrase:
        with atomic_write(path, overwrite=True) as f:
            f.write(phrase)

    if WEBVIEW and cmd in ('p.end', 'p.hypothesis') and phrase:
        body = phrase.replace(' ', '&nbsp;')
        if cmd == 'p.hypothesis':
            webview.render("<i>{{ phrase }}</i>", phrase=body)
        else:
            webview.render("{{ phrase }}", phrase=body)

    if NOTIFY and cmd == 'p.end' and phrase:
        app.notify(body=phrase)

engine.register('phrase', on_phrase)
