import time
import contextlib
from talon.voice import Context, Key, press
from talon import ctrl

ctx_global = Context("github-sitewide", bundle="org.mozilla.firefox")
ctx_repo = Context("github-repo",
                   func=lambda app, win: win.title.startswith("dwiel"))


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


# GLOBAL METHODS

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

# REPO METHODS


def repo_goto_code(m):
    page_mode()
    time.sleep(lag)
    press('g')
    time.sleep(lag)
    press('c')


def repo_goto_issues(m):
    page_mode()
    time.sleep(lag)
    press('g')
    time.sleep(lag)
    press('i')


def repo_goto_pull_requests(m):
    page_mode()
    time.sleep(lag)
    press('g')
    time.sleep(lag)
    press('p')


def repo_goto_projects(m):
    page_mode()
    time.sleep(lag)
    press('g')
    time.sleep(lag)
    press('b')


def repo_goto_wiki(m):
    page_mode()
    time.sleep(lag)
    press('g')
    time.sleep(lag)
    press('w')


ctx_global.keymap(
    {
        'jet search': search,
        '(notes | notifications)': goto_notifications,
        # '(hover)': hover

        # Reposity shortcuts; need to be moved into different file

    }
)

ctx_repo.keymap(
    {
        '[go to] code': repo_goto_code,
        '[go to] issues': repo_goto_issues,
        '[go to] (pull | pulls)[requests]': repo_goto_pull_requests,
        '[go to] projects': repo_goto_projects,
        '[go to] wiki': repo_goto_wiki
    }
)
