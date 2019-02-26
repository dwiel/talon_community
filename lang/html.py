from talon.voice import Context, Key, press
import talon.clip as clip
from ..utils import (
    text,
    parse_words,
    parse_words_as_integer,
    insert,
    word,
    join_words,
    is_filetype,
)

FILETYPES = (".html", ".jsx")

context = Context("html", func=is_filetype(FILETYPES))


def remove_spaces_around_dashes(m):
    words = parse_words(m)
    s = " ".join(words)
    s = s.replace(" – ", "-")
    insert(s)


def CursorText(s):
    left, right = s.split("{.}", 1)
    return [left + right, Key(" ".join(["left"] * len(right)))]


# Adapted from select_text_to_right_of_cursor in generic_editor.py by jcooper-korg from talon slack. Will figure out a more elegant solution later.
def skip_tag_right(m):
    key = ">"
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
    press("right", wait=0)


# Adapted from select_text_to_left_of_cursor in generic_editor.py by jcooper-korg from talon slack. Will figure out a more elegant solution later.
def skip_tag_left(m):
    old = clip.get()
    key = "<"
    press("shift-home", wait=2000)
    press("cmd-c", wait=2000)
    press("right", wait=2000)
    text_left = clip.get()
    clip.set(old)
    result = text_left.rfind(key)
    if result == -1:
        return
    # cursor over to the found key text
    for i in range(0, len(text_left) - result):
        press("left", wait=0)
    # now select the matching key text
    for i in range(0, len(key)):
        press("shift-right")
    press("left", wait=0)


context.keymap(
    {
        # Elements: Use "tag" or "ellie" as the main trigger word
        # Use this for any missing elements unti they're added
        "(tag | ellie) custom <dgndictation>": [
            "<",
            text,
            "></",
            text,
            ">",
            Key("alt-left alt-left left left"),
        ],
        "(tag | ellie) html": CursorText("<html>{.}</html>"),
        "(tag | ellie) title": CursorText("<title>{.}</title>"),
        "(tag | ellie) head": CursorText("<head>{.}</head>"),
        "(tag | ellie) body": CursorText("<body>{.}</body>"),
        "(tag | ellie) header": CursorText("<header>{.}</header>"),
        "(tag | ellie) open header": "<header>",
        "(tag | ellie) close header": "</header>",
        "(tag | ellie) main": CursorText("<main>{.}</main>"),
        "(tag | ellie) open main": "<main>",
        "(tag | ellie) close main": "</main>",
        "(tag | ellie) article": CursorText("<article>{.}</article>"),
        "(tag | ellie) open article": "<article>",
        "(tag | ellie) close article": "</article>",
        "(tag | ellie) footer": CursorText("<footer>{.}</footer>"),
        "(tag | ellie) open footer": "<footer>",
        "(tag | ellie) close footer": "</footer>",
        "(tag | ellie) div": CursorText("<div>{.}</div>"),
        "(tag | ellie) open div": "<div>",
        "(tag | ellie) close div": "</div>",
        "(tag | ellie) span": CursorText("<span>{.}</span>"),
        "(tag | ellie) open span": "<span>",
        "(tag | ellie) close span": "</span>",
        #  parse_words_as_integer doesn't seem to work so we'll do it the bad way for now
        # '(tag | ellie) heading <dgndictation>': ['<h', parse_words_as_integer, '></h', parse_words_as_integer, '>'],
        "(tag | ellie) heading one": CursorText("<h1>{.}</h1>"),
        "(tag | ellie) heading two": CursorText("<h2>{.}</h2>"),
        "(tag | ellie) heading three": CursorText("<h3>{.}</h3>"),
        "(tag | ellie) heading four": CursorText("<h4>{.}</h4>"),
        "(tag | ellie) heading five": CursorText("<h5>{.}</h5>"),
        "(tag | ellie) heading six": CursorText("<h6>{.}</h6>"),
        "((tag | ellie) paragraph | (tag | ellie) pee)": CursorText("<p>{.}</p>"),
        "((tag | ellie) yule | (tag | ellie) un-list | (tag | ellie) un-ordered list)": CursorText(
            "<ul>{.}</ul>"
        ),
        "((tag | ellie) open un-ordered list | (tag | ellie) open un-list)": "<ul>",
        "((tag | ellie) close un-ordered list | (tag | ellie) close un-list)": "</ul>",
        "((tag | ellie) list item | (tag | ellie) lie)": CursorText("<li>{.}</li>"),
        "((tag | ellie) open list item | (tag | ellie) open lie)": "<li>",
        "((tag | ellie) close list item | (tag | ellie) close lie)": "</li>",
        "(tag | ellie) link": CursorText('<a href="" alt="">{.}</a>'),
        "(tag | ellie) open link": CursorText('<a href="{.}" alt="">'),
        "(tag | ellie) close link": CursorText("{.}</a>"),
        "(tag | ellie) image": CursorText('<img src="{.}" alt="" title="" />'),
        "(tag | ellie) her": "<hr>",
        "(tag | ellie) burr": "<br>",
        # Attributes - example: "tag div addy class box" will output "<div class="box"></div>
        "addy class <dgndictation>": [
            Key("left"),
            ' class=""',
            Key("left"),
            remove_spaces_around_dashes,
            Key("right right"),
        ],
        "addy ID <dgndictation>": [
            Key("left"),
            ' id=""',
            Key("left"),
            remove_spaces_around_dashes,
            Key("right right"),
        ],
        # Moving Around between tags
        "skip (tag | ellie) right": skip_tag_right,
        "skip (tag | ellie) left": skip_tag_left,
    }
)
