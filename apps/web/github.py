import time
import contextlib
from talon.voice import Context, Key, press
from talon import ctrl

ctx_global = Context("github-sitewide", bundle="org.mozilla.firefox")
ctx_repo = Context("github-repo",
                   func=lambda app, win: in_repo_list(win.title))
ctx_editor = Context("github-code-editor",
                     func=lambda app, win: win.title.startswith("Editing"))
ctx_issues_pull_lists = Context("github-issues-pull-requests_lists",
                                func=lambda app, win:
                                win.title.startswith("Issues") or
                                win.title.startswith("Pull Requests"))
ctx_issues_pull = Context("github-issues-pull-requests",
                          func=lambda app, win:
                          " Issue " in win.title or
                          " Pull Request " in win.title)
ctx_pull_changes = Context("github-pull-request-changes",
                           func=lambda app, win:
                           " Pull Request " in win.title)
ctx_network_graph = Context("github-network-graph",
                            func=lambda app, win:
                            win.title.startswith("Network Graph"))

# USER-DEFINED VARIABLES

repos = {"talon_community"}

lag = 0.2
using_tridactyl = True


def in_repo_list(win_title):
    for repo in repos:
        if repo in win_title:
            return True
    return False


def normal_mode():
    # get out of any text box
    time.sleep(lag)
    press('escape')
    time.sleep(lag)


def tridactyl_mode():
    if using_tridactyl:
        # normal_mode()
        time.sleep(lag)
        press("ctrl-alt-escape")
        time.sleep(lag)


def page_mode():
    normal_mode()
    if using_tridactyl:
        press("ctrl-alt-escape")
        time.sleep(lag)


# SITE-WIDE METHODS

def search(m):
    page_mode()
    press('/')


def goto_notifications(m):
    page_mode()
    press('g')
    time.sleep(lag)
    press('n')
    tridactyl_mode()

# REPO METHODS


def repo_goto_code(m):
    page_mode()
    press('g')
    time.sleep(lag)
    press('c')
    tridactyl_mode()


def repo_goto_issues(m):
    page_mode()
    press('g')
    time.sleep(lag)
    press('i')
    tridactyl_mode()


def repo_goto_pull_requests(m):
    page_mode()
    press('g')
    time.sleep(lag)
    press('p')
    tridactyl_mode()


def repo_goto_projects(m):
    page_mode()
    press('g')
    time.sleep(lag)
    press('b')
    tridactyl_mode()


def repo_goto_wiki(m):
    page_mode()
    press('g')
    time.sleep(lag)
    press('w')
    tridactyl_mode()


def repo_find_file(m):
    page_mode()
    press('t')


def repo_switch_branch(m):
    page_mode()
    press('w')

# ISSUES AND PULL REQUESTS LISTS METHODS


def create_issue(m):
    page_mode()
    press('c')


def filter_by_author(m):
    page_mode()
    press('u')


def filter_by_label(m):
    page_mode()
    press('l')


def filter_by_milestone(m):
    page_mode()
    press('m')


def filter_by_assignee(m):
    page_mode()
    press('a')


def open_issue(m):
    page_mode()
    press('o')
    tridactyl_mode()


# ISSUES AND PULL REQUESTS METHODS


def request_reviewer(m):
    page_mode()
    press('q')


def set_milestone(m):
    page_mode()
    press('m')


def apply_label(m):
    page_mode()
    press('l')


def set_assignee(m):
    page_mode()
    press('a')


# PULL REQUEST CHANGES METHODS

def list_commits(m):
    page_mode()
    press('c')


def list_changed_files(m):
    page_mode()
    press('t')

# NETWORK GRAPH METHODS


def scroll_left(m):
    page_mode()
    press('h')
    tridactyl_mode()


def scroll_right(m):
    page_mode()
    press('l')
    tridactyl_mode()


def scroll_down(m):
    page_mode()
    press('j')
    tridactyl_mode()


def scroll_up(m):
    page_mode()
    press('k')
    tridactyl_mode()


def scroll_left_most(m):
    page_mode()
    press('shift-h')
    tridactyl_mode()


def scroll_right_most(m):
    page_mode()
    press('shift-l')
    tridactyl_mode()


def scroll_down_most(m):
    page_mode()
    press('shift-j')
    tridactyl_mode()


def scroll_up_most(m):
    page_mode()
    press('shift-k')
    tridactyl_mode()


ctx_global.keymap(
    {
        'jet search': search,
        '(notes | notifications)': goto_notifications,
        # '(hover)': hover
    }
)

ctx_repo.keymap(
    {
        '[go to] code': repo_goto_code,
        '[go to] issues': repo_goto_issues,
        '[go to] (pull | pulls)[requests]': repo_goto_pull_requests,
        '[go to] projects': repo_goto_projects,
        '[go to] wiki': repo_goto_wiki,
        'find file': repo_find_file,
        'switch [(branch | tag)]': repo_switch_branch
    }
)

ctx_editor.keymap(
    {
        '(search | find)': Key('cmd-f'),
        '[find] next': Key('cmd-g'),
        '[find] prev': Key('shift-cmd-g'),
        'replace': Key('cmd-alt-f'),
        'replace all': Key('shift-cmd-alt-f'),
        '(go to | jump to) [line]': Key('alt-g'),
        'undo': Key('cmd-z'),
        'redo': Key('cmd-y')
    }
)

ctx_issues_pull_lists.keymap(
    {
        'create [issue] [pull request]': create_issue,
        '[filter] [by] author': filter_by_author,
        '[filter] [by] label': filter_by_label,
        '[filter] [by] milestone': filter_by_milestone,
        '[filter] [by] [(worker | assigned | assignee)]': filter_by_assignee,
        'open [issue] [pull request]': open_issue
    }
)

ctx_issues_pull.keymap(
    {
        '[request] (reviewer | review)': request_reviewer,
        '[set] milestone': set_milestone,
        '[apply] label': apply_label,
        'assign': set_assignee
    }
)

ctx_pull_changes.keymap(
    {
        '[list] commits': list_commits,
        '[list] [changed] files': list_changed_files,
        'down': Key('j'),
        'up': Key('k'),
        '[add] [diff] comment': Key('cmd-shift-enter')
    }
)

ctx_network_graph.keymap(
    {
        '[scroll] left': scroll_left,
        '[scroll] right': scroll_right,
        '[scroll] down': scroll_down,
        '[scroll] up': scroll_up,
        '[scroll] left most': scroll_left_most,
        '[scroll] right most': scroll_right_most,
        '[scroll] down most': scroll_down_most,
        '[scroll] up most': scroll_up_most,
    }
)
