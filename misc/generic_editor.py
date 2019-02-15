# https://github.com/JonathanNickerson/talon_voice_user_scripts
# TODO tidy this file

import time

import talon.clip as clip
from talon.voice import Key, press, Str, Context
from ..utils import parse_words, join_words, numerals, optional_numerals, is_not_vim, text_to_number

ctx = Context("generic_editor", func=is_not_vim)

def jump_to_bol(words):
    line = text_to_number(words)
    press("cmd-l")
    Str(str(line))(None)
    press("enter")

def select_line(m):
    jump_to_bol(m._words[1:])


def jump_to_end_of_line():
    press("cmd-right")


def jump_to_beginning_of_text():
    press("cmd-left")


def jump_to_nearly_end_of_line():
    press("left")


def jump_to_bol_and(then):
    def fn(m):
        if len(m._words) > 1:
            jump_to_bol(m._words[1:])
        else:
            press("ctrl-a")
            press("cmd-left")
        then()

    return fn


def jump_to_eol_and(then):
    def fn(m):
        if len(m._words) > 1:
            jump_to_bol(m._words[1:])
        press("cmd-right")
        then()

    return fn


def snipline():
    press("shift-cmd-right")
    press("delete")
    press("delete")
    press("ctrl-a")
    press("cmd-left")


def find_next(m):
    press("cmd-f")
    Str(str(m.dgndictation[0]._words[0]))(None)
    press("escape")


def find_previous(m):
    press("left")
    press("cmd-f")
    Str(str(m.dgndictation[0]._words[0]))(None)
    press("cmd-shift-g")
    press("escape")


# jcooper-korg from talon slack
def select_text_to_left_of_cursor(m):
    words = parse_words(m)
    if not words:
        return
    old = clip.get()
    key = join_words(words).lower()
    press("shift-home", wait=2000)
    press("cmd-c", wait=2000)
    press("right", wait=2000)
    text_left = clip.get()
    clip.set(old)
    result = text_left.find(key)
    if result == -1:
        return
    # cursor over to the found key text
    for i in range(0, len(text_left) - result):
        press("left", wait=0)
    # now select the matching key text
    for i in range(0, len(key)):
        press("shift-right")


# jcooper-korg from talon slack
def select_text_to_right_of_cursor(m):
    words = parse_words(m)
    if not words:
        return
    key = join_words(words).lower()
    old = clip.get()
    press("shift-end", wait=2000)
    press("cmd-c", wait=2000)
    press("left", wait=2000)
    text_right = clip.get()
    clip.set(old)
    result = text_right.find(key)
    if result == -1:
        return
    # cursor over to the found key text
    for i in range(0, result):
        press("right", wait=0)
    # now select the matching key text
    for i in range(0, len(key)):
        press("shift-right")


alphanumeric = "abcdefghijklmnopqrstuvwxyz0123456789_"


def word_neck(m):
    # print(m)
    word_index = text_to_number(m._words[1:])
    if not word_index:
        word_index = 1

    old = clip.get()
    press("shift-right", wait=2000)
    press("cmd-c", wait=2000)
    press("shift-left", wait=2000)
    current_highlight = clip.get()
    if len(current_highlight) > 1:
        press("right", wait=2000)
    press("shift-end", wait=2000)
    time.sleep(0.25)
    press("cmd-c", wait=2000)
    press("left", wait=2000)
    time.sleep(0.25)
    text_right = clip.get().lower()
    clip.set(old)

    is_word = [character in alphanumeric for character in text_right]
    word_count = 1
    i = 0
    while i < (len(is_word) - 1) and not is_word[i]:
        i += 1

    # print("a start", i)

    while i < (len(is_word) - 1) and word_count < word_index:
        # print(i, is_word[i], word_count, word_index)
        if not is_word[i] and is_word[i + 1]:
            word_count += 1
        i += 1
    # warning: this is a hack, sorry
    # print("i", i)
    if i == 1 and is_word[0]:
        i = 0
    start_position = i
    # print(text_right[start_position:])
    while i < len(is_word) and is_word[i]:
        i += 1
    end_position = i

    # print(start_position, end_position)
    # cursor over to the found word
    for i in range(0, start_position):
        press("right", wait=0)
    # now select the word
    for i in range(0, end_position - start_position):
        press("shift-right")


def word_prev(m):
    word_index = text_to_number(m._words[1:])
    if not word_index:
        word_index = 1

    old = clip.get()
    press("shift-right", wait=2000)
    press("cmd-c", wait=2000)
    press("shift-left", wait=2000)
    current_highlight = clip.get()
    if len(current_highlight) > 1:
        press("left", wait=2000)
    press("shift-home", wait=2000)
    time.sleep(0.25)
    press("cmd-c", wait=2000)
    press("right", wait=2000)
    time.sleep(0.25)
    text_right = clip.get().lower()
    clip.set(old)

    text_right = list(reversed(text_right))

    is_word = [character in alphanumeric for character in text_right]
    word_count = 1
    i = 0
    while i < (len(is_word) - 1) and not is_word[i]:
        i += 1

    while i < (len(is_word) - 1) and word_count < word_index:
        # print(i, is_word[i], word_count, word_index)
        if not is_word[i] and is_word[i + 1]:
            word_count += 1
        i += 1
    start_position = i
    # print(text_right[start_position:])
    while i < len(is_word) and is_word[i]:
        i += 1
    end_position = i

    # print(start_position, end_position, text_right[start_position:end_position])
    # cursor over to the found word
    for i in range(0, start_position):
        press("left", wait=0)
    # now select the word
    for i in range(0, end_position - start_position):
        press("shift-left")


ctx.keymap({
    # META
    "sage": Key("cmd-s"),
    "dizzle": Key("cmd-z"),
    "rizzle": Key("cmd-shift-z"),

    # MOTIONS
    'spring' + optional_numerals: jump_to_eol_and(jump_to_beginning_of_text),
    'dear' + optional_numerals: jump_to_eol_and(lambda: None),
    'smear' + optional_numerals: jump_to_eol_and(jump_to_nearly_end_of_line),
    'sprinkoon' + numerals: jump_to_eol_and(lambda: press('enter')),
    "shockey": Key("ctrl-a cmd-left enter up"),
    "shockoon": Key("cmd-right enter"),

    'jolt': Key('ctrl-a cmd-left shift-down cmd-c down cmd-v' ), # duplicate line

    # DELETING
    "snipple": Key("shift-cmd-left delete"),
    "snipper": Key("shift-cmd-right delete"),
    "shackle": Key("cmd-right shift-cmd-left"),
    'snipline' + optional_numerals: jump_to_bol_and(snipline),

    # SELECTING
    'sprinkle' + optional_numerals: select_line,
    "crew <dgndictation>": select_text_to_right_of_cursor,
    "trail <dgndictation>": select_text_to_left_of_cursor,
    "shift home": Key("shift-home"),
    "wordneck" + optional_numerals: word_neck,
    "wordprev" + optional_numerals: word_prev,
    "word this": [Key("alt-right"), Key("shift-alt-left")],
})
