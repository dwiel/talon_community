import time
import contextlib
from talon.voice import Context, Key, press
from talon import ctrl

def normal_mode():
    # get out of any text box
    press('escape')
    # make sure we are in normal mode
    press('escape')

def page_mode():
    normal_mode()
    # insert ignore mode
    press("ctrl-alt-escape")

@contextlib.contextmanager
def page_mode_context():
    page_mode()
    yield
    normal_mode()

def send_string_to_page(string=None):
    def function(m):
        with page_mode_context():
            time.sleep(0.3)
            for character in string:
                press(character)
    return function

def send_key_to_page(key=None):
    def function(m):
        with page_mode_context():
            time.sleep(0.3)
            press(key)
    return function

def compose(m):
    page_mode()

ctx = Context("gmail", func=lambda app, win: win.title.endswith("- Gmail"))
ctx.keymap(
    {
        # Comompose and Chat Commands
        "inbox": send_string_to_page("gi"),
        "help" : send_key_to_page('shift-?'),
        "search mail" : send_key_to_page('/')
        "compose new tab" : send_key_to_page('d'),   
        "previous message" : send_key_to_page('p'),
        "next message" : send_key_to_page('n'),
        "focus main window" : send_key_to_page('shift-escape'),
        "focus latest chat" : send_key_to_page('escape'),
        "advance to next chat" : send_key_to_page('ctrl-.'),
        "advance to previous chat" : send_key_to_page('ctrl-,'),
        "send" : send_key_to_page('ctrl-enter'),
        "send" : send_key_to_page('cmd-enter'),
        "add cc" : send_key_to_page('ctrl-shift-c'),
        "add cc" : send_key_to_page('cmd-shift-c'),
        "add bcc" : send_key_to_page('ctrl-shift-b'),
        "add bcc" : send_key_to_page('cmd-shift-b'),
        "access custom form" : send_key_to_page('ctrl-shift-f'),
        "access custom form" : send_key_to_page('cmd-shift-f'),
        "insert link" : send_key_to_page('ctrl-k'),
        "insert link" : send_key_to_page('cmd-k'),
        "go to next misspelled word" : send_key_to_page('cmd-;'),
        "open spelling suggestions" : send_key_to_page('ctrl-m'),
        # Formatting Text
        "previous font" : send_key_to_page('ctrl-shift-5'),
        "next font" : send_key_to_page('ctrl-shift-6'),
        "decrease text size" : send_key_to_page('ctrl-shift--'),
        "increase text size" : send_key_to_page('ctrl-shift-+'),
        "bold" : send_key_to_page('ctrl-b'),
        "italic" : send_key_to_page('ctrl-i'),
        "underline" : send_key_to_page('ctrl-u'),
        "numbered list" : send_key_to_page('ctrl-shift-7'),
        "bulleted list" : send_key_to_page('ctrl-shift-8'),
        "quote" : send_key_to_page('ctrl-shift-9'),
        "indent less" : send_key_to_page('ctrl-shift-['),
        "indent more" : send_key_to_page('ctrl-shift-]'),
        "align left" : send_key_to_page('ctrl-shift-l'),
        "align center" : send_key_to_page('ctrl-shift-e'),
        "align right" : send_key_to_page('ctrl-shift-r'),
        "remove formatting" : send_key_to_page('ctrl-\'),
        "previous font" : send_key_to_page('cmd-shift-5'),
        "next font" : send_key_to_page('cmd-shift-6'),
        "decrease text size" : send_key_to_page('cmd-shift--'),
        "increase text size" : send_key_to_page('cmd-shift-+'),
        "bold" : send_key_to_page('cmd-b'),
        "italic" : send_key_to_page('cmd-i'),
        "underline" : send_key_to_page('cmd-u'),
        "numbered list" : send_key_to_page('cmd-shift-7'),
        "bulleted list" : send_key_to_page('cmd-shift-8'),
        "quote" : send_key_to_page('cmd-shift-9'),
        "indent less" : send_key_to_page('cmd-shift-['),
        "indent more" : send_key_to_page('cmd-shift-]'),
        "align left" : send_key_to_page('cmd-shift-l'),
        "align center" : send_key_to_page('cmd-shift-e'),
        "align right" : send_key_to_page('cmd-shift-r'),
        "remove formatting" : send_key_to_page('cmd-\'),
        # Actions
        "focus toolbar" : send_key_to_page(','),
        "select conversation" : send_key_to_page('x'),
        "(toggle star | rotate among superstars" : send_key_to_page('s'),
        "archive" : send_key_to_page('e'),
        "mute conversation" : send_key_to_page('m'),
        "report spam" : send_key_to_page('!'),
        "delete" : send_key_to_page('#'),
        "reply" : send_key_to_page('r'),
        "reply in new window" : send_key_to_page('shift-r'),
        "reply all" : send_key_to_page('a'),
        "replay all in new window" : send_key_to_page('shift-a'),
        "forward" : send_key_to_page('f'),
        "forward in new window" : send_key_to_page('shift-f'),
        "update conversation" : send_key_to_page('shift-n'),
        "archive conversation and previous" : send_key_to_page(']'),
        "archive conversation and next" : send_key_to_page('['),
        "mark unread from selected message" : send_key_to_page('_'),
        "mark as important" : send_key_to_page('+'),
        "mark as important" : send_key_to_page('='),
        "mark as not important" : send_key_to_page('-'),
        "snooze" : send_key_to_page('b'),
        "expand entire conversation" : send_key_to_page(';'),
        "collapse entire conversation" : send_key_to_page(':'),
        "add conversation to task" : send_key_to_page('shift-t'),
        # Hangout
        "show menu" : send_key_to_page('h-m'),
        "show archived hangouts" : send_key_to_page('h-a'),
        "show hangout requests" : send_key_to_page('h-i'),
        "focus conversation list" : send_key_to_page('h-c'),
        "open phone" : send_key_to_page('g-p'),
        "open phone" : send_key_to_page('h-p'),
        # Jumping
        "go to inbox" : send_key_to_page('g-i'),
        "go to starred conversations" : send_key_to_page('g-s'),
        "go to sent messages" : send_key_to_page('g-t'),
        "go to drafts" : send_key_to_page('g-d'),
        "go to all mail" : send_key_to_page('g-a'),
        "switch to inbox" : send_key_to_page('ctrl-alt-,'),
        "switch to inbox" : send_key_to_page('cmd-alt-,'),
        "switch from inbox" : send_key_to_page('ctrl-alt-.'),
        "switch from inbox" : send_key_to_page('cmd-alt-.'),
        "go to tasks" : send_key_to_page('g-k'),
        "go to label" : send_key_to_page('g-l'),
        # Threadlist Selection
        "select all conversation" : send_key_to_page('*-a'),
        "deselect all conversation" : send_key_to_page('*-n'),
        "select read conversation" : send_key_to_page('*-r'),
        "select unread conversation" : send_key_to_page('*-u'),
        "select starred conversation" : send_key_to_page('*-s'),
        "select unstarred conversation" : send_key_to_page('*-t'),
        # Navigation
        "back to threadlist" : send_key_to_page('u'),
        "newer conversation" : send_key_to_page('k'),
        "older conversation" : send_key_to_page('j'),
        "open conversation" : send_key_to_page('o'),
        "open conversation" : send_key_to_page('\''),
        "go to next inbox section" : send_key_to_page('o'),
        "go to previous inbox section" : send_key_to_page('~'),
        # Application
        "compose" : send_key_to_page('c'),
        "compose in new tab" : send_key_to_page('d'),
        "search msil" : send_key_to_page('/'),
        "search chat contacts" : send_key_to_page('g'),
        "open more actions" : send_key_to_page('.'),
        "open move to" : send_key_to_page('v'),
        "open label as" : send_key_to_page('l'),
        "open keyboard shortcut help" : send_key_to_page('?'),





sasabrihya
salma









    }
)
