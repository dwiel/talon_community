from talon.voice import Context, Key, engine, Str
from ..utils import parse_word

ctx = Context('keeper')

def keeper(j):
    if j['cmd'] == 'p.end' and j['grammar'] == 'talon':
        phrase = j['phrase']
        if phrase and phrase[0] == 'keeper':
            # Str(' '.join(map(parse_word, phrase[1:])))(None)
            Str(' '.join(phrase[1:]))(None)
            return False

engine.register('pre:phrase', keeper)
ctx.keymap({
    'keeper [<dgndictation>]': lambda m: None,
})
