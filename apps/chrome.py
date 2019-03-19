import time

from .. import utils
from .web import browser

from talon import ui
from talon.voice import Context, Key, Str, press

# It is recommended to use this script in tandem with Vimium, a Google Chrome plugin for controlling the browser via keyboard
# https://vimium.github.io/

context = Context("GoogleChrome", bundle="com.google.Chrome")


def get_url(win=None):
    if win is None:
        win = ui.active_window()
    return tuple(win.children.find(AXTitle="Address and search bar"))[0].AXValue
    # win.children.find(AXTitle='Address and search bar')[0].AXValue


def set_url(url, win=None):
    if win is None:
        win = ui.active_window()
    focus_address_bar()
    utils.paste_text(url)


def navigate_to_url(url, win=None):
    set_url(url, win)
    press("enter")


def open_focus_devtools(m):
    press("cmd-shift-c")


def show_panel(name):
    open_focus_devtools(None)

    # Open command menu
    press("cmd-shift-p")

    Str("Show %s" % (name))(None)
    press("enter")


def next_panel(m):
    open_focus_devtools(None)
    press("cmd-]")


def last_panel(m):
    open_focus_devtools(None)
    press("cmd-[")


def focus_address_bar(m=None):
    press("cmd-l")


# Return focus from the devtools to the page
def refocus_page(m):
    focus_address_bar(None)
    time.sleep(0.1)
    press("escape")
    press("escape")
    # time.sleep(0.1)
    # This leaves the focus on the page at previous tab focused point, not the beginning of the page
    press("tab")


def back(m):
    refocus_page(None)
    press("cmd-[")
    # refocus_page(None)


def forward(m):
    refocus_page(None)
    press("cmd-]")
    refocus_page(None)


def link(m):
    refocus_page(None)
    press("f")


def jump_tab(m):
    tab_number = utils.parse_words_as_integer(m._words[1:])
    if tab_number is not None and tab_number > 0 and tab_number < 9:
        press("cmd-%s" % tab_number)


def mendeley(m):
    navigate_to_url(f"https://www.mendeley.com/import/?url={get_url()}")


context.keymap(
    {
        "(address bar | focus address | focus url | url)": focus_address_bar,
        "copy url": Key("escape y y"),
        "go back": back,
        "go forward": forward,
        "reload": Key("cmd-r"),
        "hard reload": Key("cmd-shift-r"),
        "new tab": Key("cmd-t"),
        "close tab": Key("cmd-w"),
        "(reopen | unclose) tab": Key("cmd-shift-t"),
        "(next tab | goneck)": Key("cmd-shift-]"),
        "((last | previous | preev) tab | gopreev)": Key("cmd-shift-["),
        "tab (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8)": jump_tab,
        "(end | rightmost) tab": Key("cmd-9"),
        "marco": Key("cmd-f"),
        "marneck": Key("cmd-g"),
        "(last | prevous)": Key("cmd-shift-g"),
        "toggle dev tools": Key("cmd-alt-i"),
        "command menu": Key("cmd-shift-p"),
        "next panel": next_panel,
        "(last | previous) panel": last_panel,
        "show application [panel]": lambda m: show_panel("Application"),
        "show audit[s] [panel]": lambda m: show_panel("Audits"),
        "show console [panel]": lambda m: show_panel("Console"),
        "show element[s] [panel]": lambda m: show_panel("Elements"),
        "show memory [panel]": lambda m: show_panel("Memory"),
        "show network [panel]": lambda m: show_panel("Network"),
        "show performance [panel]": lambda m: show_panel("Performance"),
        "show security [panel]": lambda m: show_panel("Security"),
        "show source[s] [panel]": lambda m: show_panel("Sources"),
        "(refocus | focus) page": refocus_page,
        "[refocus] dev tools": open_focus_devtools,
        # Clipboard
        "cut": Key("cmd-x"),
        "copy": Key("cmd-c"),
        "paste": Key("cmd-v"),
        "paste same style": Key("cmd-alt-shift-v"),
        # "mendeley": Key("cmd-shift-m"),
        "(add | save) to mendeley": mendeley,
        # TODO: this should probably be specific to the page
        "submit": Key("cmd-enter"),
        # zotero
        "zotero": Key("cmd-shift-z"),
        # rearrange tabs: https://chrome.google.com/webstore/detail/rearrange-tabs/ccnnhhnmpoffieppjjkhdakcoejcpbga
        # "move tab left": Key("ctrl-shift-left"),
        # "move tab right": Key("ctrl-shift-right"),
        # "move tab left way": Key("ctrl-shift-down"),
        # vimium
        "link": link,
        "move tab left": browser.send_to_vimium("<<"),
        "move tab right": browser.send_to_vimium(">>"),
    }
)
