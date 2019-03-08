from talon.voice import Context, engine
from ..utils import remove_dragon_junk, insert, join_words

ctx = Context("keeper")

keeper_phrase = None


def keeper(j):
    global keeper_phrase

    if j["cmd"] == "p.end" and j["grammar"] == "talon":
        phrase = j["phrase"]
        if phrase:
            keeper_phrase = None
            if "keeper" in phrase:
                i = phrase.index("keeper")
                keeper_phrase = join_words(map(remove_dragon_junk, phrase[i + 1 :]))
                j["parsed"] = j["parsed"][:i]


def keeper_post(j):
    global keeper_phrase
    if j["cmd"] == "p.end" and j["grammar"] == "talon":
        phrase = j["phrase"]
        if phrase:
            if keeper_phrase:
                insert(keeper_phrase)
                keeper_phrase = None


engine.register("pre:phrase", keeper)
engine.register("post:phrase", keeper_post)
ctx.keymap({"keeper [<dgndictation>]": lambda m: None})
