import time
import contextlib
from talon.voice import Context, Key, press
from talon import ctrl

ctx = Context("github-sitewide", bundle="org.mozilla.firefox")

# seconds to wait between keypresses
lag = 0.3


def normal_mode():
    # get out of any text box
    time.sleep(lag)
    press('escape')


def page_mode():
    normal_mode()
    time.sleep(lag)
    # insert ignore mode
    press("ctrl-alt-escape")


def search(m):
    page_mode()
    time.sleep(lag)
    press('/')


def goto_notifications(m):
    page_mode()
    time.sleep(lag)
    press('g')
    time.sleep(lag)
    press('n')


def goto_code(m):
    page_mode()
    time.sleep(lag)
    press('g')
    time.sleep(lag)
    press('c')


def goto_issues(m):
    page_mode()
    time.sleep(lag)
    press('g')
    time.sleep(lag)
    press('i')


ctx.keymap(
    {
        'jet search': search,
        '(notes | notifications)': goto_notifications,
        # '(hover)': hover

        # Reposity shortcuts; need to be moved into different file
        '[go to] code': goto_code,
        '[go to] issues': goto_issues
    }
)
