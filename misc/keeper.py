from talon.voice import Context, engine
from ..utils import remove_dragon_junk, insert, join_words

ctx = Context("keeper")


def keeper(j):
    if j["cmd"] == "p.end" and j["grammar"] == "talon":
        phrase = j["phrase"]
        if phrase and phrase[0] == "keeper":
            insert(join_words(map(remove_dragon_junk, phrase[1:])))(None)
            j["cmd"] = "p.skip"


engine.register("pre:phrase", keeper)
ctx.keymap({"keeper [<dgndictation>]": lambda m: None})
