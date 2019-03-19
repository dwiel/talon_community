"""
when someone has the time to help debug, message aegis

    aegis [11:40 AM]
    You can do vars(user.whatever.speech_toggle.dictation_group) while you’re in dictation mode
    Where whatever is the intermediate python
"""

from talon.voice import Str, Key
from talon import ui

from .speech_toggle import dictation

# cleans up some Dragon output from <dgndictation>
mapping = {"semicolon": ";", "new-line": "\n", "new-paragraph": "\n\n"}
# used for auto-spacing
punctuation = set(".,-!?")
sentence_ends = set(".!?").union({"\n", "\n\n"})


def insert(s):
    Str(s)(None)


class AutoFormat:
    def __init__(self):
        self.reset()
        ui.register("app_deactivate", lambda app: self.reset())
        ui.register("win_focus", lambda win: self.reset())

    def reset(self):
        self.caps = True
        self.space = False

    def insert_word(self, word):
        word = str(word).lstrip("\\").split("\\", 1)[0]
        word = mapping.get(word, word)
        word = word.rstrip("-")

        if self.caps:
            word = word[0].upper() + word[1:]

        if self.space and word[0] not in punctuation and "\n" not in word:
            insert(" ")

        insert(word)

        self.caps = word in sentence_ends
        self.space = "\n" not in word

    def phrase(self, m):
        for word in m.dgndictation[0]:
            self.insert_word(word)


auto_format = AutoFormat()
dictation.keymap({"<dgndictation>": auto_format.phrase, "press enter": Key("enter")})
