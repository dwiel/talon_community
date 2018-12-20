import time
import contextlib
from talon.voice import Context, Key, press
from talon import ctrl

ctx = Context("github-sitewide", bundle="org.mozilla.firefox")


def normal_mode():
    # get out of any text box
    press('escape')
    time.sleep(0.1)
    # make sure we are in normal mode
    press('escape')


def page_mode():
    normal_mode()
    time.sleep(0.1)
    # insert ignore mode
    press("ctrl-alt-escape")


def search(m):
    page_mode()
    press('/')


def notifications(m):
    page_mode()
    time.sleep(0.1)
    press('g')
    time.sleep(0.1)
    press('n')


ctx.keymap(
    {
        'jet search': search,
        'notes': notifications
    }
)
