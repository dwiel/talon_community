import time
import glob
import os

from .. import utils
from .. import config
from .web import browser
from ..misc import switcher

from talon import ui, ctrl
from talon.voice import Context, Key, Str, press

# It is recommended to use this script in tandem with Vimium, a Google Chrome plugin for controlling the browser via keyboard
# https://vimium.github.io/

context = Context("GoogleChrome", bundle="com.google.Chrome")


def most_recently_downloaded_file():
    list_of_files = glob.glob(os.path.expanduser("~/Downloads/*"))
    return max(list_of_files, key=os.path.getctime)


def open_most_recently_downloaded_file(m):
    os.system(f"open {most_recently_downloaded_file()}")


def get_url(win=None):
    if win is None:
        win = ui.active_window()
    children = win.children.find(AXRole="AXTextField")
    if children:
        return children[0].AXValue
    else:
        return None


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


def new_tab(m):
    print("hidden", ui.active_window().hidden)
    print(ui.active_window().children)
    if not ui.active_window().hidden:
        press("cmd-t")
    else:
        press("cmd-n")


def next_panel(m):
    open_focus_devtools(None)
    press("cmd-]")


def last_panel(m):
    open_focus_devtools(None)
    press("cmd-[")


def focus_address_bar(m=None):
    press("cmd-l")
    time.sleep(0.1)


# Return focus from the devtools to the page
def refocus_page(m):
    focus_address_bar(None)
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
    time.sleep(0.1)
    press("cmd-right")
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


webpages = config.load_config_json("webpages.json")


def get_webpage(m):
    return webpages[" ".join(m["global_browser.webpages"])]


def new_tab_go_to_webpage(m):
    press("cmd-t")
    navigate_to_url(get_webpage(m))


def go_to_webpage(m):
    navigate_to_url(get_webpage(m))


def get_search(m, default="google"):
    key = " ".join(m["global_browser.searches"])
    if key in searches:
        return searches[key]
    else:
        return default


searches = config.load_config_json("searches.json")


def new_search_new_tab(m):
    press("cmd-t")
    utils.insert(get_search(m))
    press("tab")
    search_text = utils.join_words(utils.parse_words(m))
    if search_text:
        print(search_text)
        utils.insert(search_text)
        press("enter")


def new_search_existing_tab(m):
    press("cmd-l")
    utils.insert(get_search(m))
    press("tab")
    search_text = utils.join_words(utils.parse_words(m))
    if search_text:
        print(search_text)
        utils.insert(search_text)
        press("enter")


def open_way_back_machine(m):
    browser.navigate_to_url(f"http://web.archive.org/web/{browser.get_url()}")


context.keymap(
    {
        "(address bar | focus address | focus url | url)": focus_address_bar,
        "copy url": Key("escape y y"),
        "go back": back,
        "go forward": forward,
        "page reload": Key("cmd-r"),
        "reload page": Key("cmd-r"),
        "hard reload": Key("cmd-shift-r"),
        "new tab": new_tab,
        "new tab {global_browser.webpages}": new_tab_go_to_webpage,
        "go {global_browser.webpages}": go_to_webpage,
        "new search [{global_browser.searches}] [<dgndictation>]": new_search_new_tab,
        "go search [{global_browser.searches}] [<dgndictation>]": new_search_existing_tab,
        "search {global_browser.searches} [<dgndictation>]": new_search_existing_tab,
        "close tab": Key("cmd-w"),
        "(reopen | unclose) tab": Key("cmd-shift-t"),
        "(next tab | goneck)": Key("cmd-shift-]"),
        "((last | previous | preev) tab | gopreev)": Key("cmd-shift-["),
        "tab (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8)": jump_tab,
        "(end | rightmost) tab": Key("cmd-9"),
        "marco": Key("cmd-f"),
        "marneck": Key("cmd-g"),
        "marprev": Key("cmd-shift-g"),
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
        # "cut": Key("cmd-x"),
        # "copy": Key("cmd-c"),
        # "paste": Key("cmd-v"),
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
        "open link": link,
        "move tab left": browser.send_to_vimium("<<"),
        "move tab right": browser.send_to_vimium(">>"),
        "move tab new window": browser.send_to_vimium("W"),
        "tab (named | name | by name)": browser.send_to_vimium("T"),
        "tab (named | name | by name) <dgndictation>": [
            browser.send_to_vimium("T"),
            lambda m: time.sleep(0.3),
            lambda m: utils.paste_text(utils.string_capture(m)),
            lambda m: time.sleep(0.0),
            Key("enter"),
        ],
        "pin tab": Key("alt-p"),
        "open most recently downloaded file": open_most_recently_downloaded_file,
        # archive.org
        "open [in] (way back [machine] | archive)": open_way_back_machine,
    }
)


def global_chrome_new_tab(m):
    switcher.switch_app(name="Google Chrome")
    press("cmd-t")


def global_go_to_webpage(m):
    switcher.switch_app(name="Google Chrome")
    new_tab_go_to_webpage(m)


def global_chrome_new_search(m):
    switcher.switch_app(name="Google Chrome")
    new_search_new_tab(m)


def global_chrome_close_tab(m):
    current_app = ui.active_window().app
    switcher.switch_app(name="Google Chrome")
    press("cmd-w")
    current_app.focus()
    # app = ui.apps(bundle="com.google.Chrome")[0]
    # ctrl.key_press("w", cmd=True, app=app)


global_ctx = Context("global_browser")
global_ctx.set_list("webpages", webpages.keys())
global_ctx.set_list("searches", searches.keys())
global_ctx.keymap(
    {
        "chrome new tab": global_chrome_new_tab,
        "chrome new [tab] {global_browser.webpages}": global_go_to_webpage,
        "chrome close tab": global_chrome_close_tab,
        "chrome search [<dgndictation>]": [global_chrome_new_tab, utils.text, " "],
        "chrome lucky [<dgndictation>]": [
            global_chrome_new_tab,
            "lucky ",
            utils.text,
            " ",
        ],
        "chrome {global_browser.searches} [<dgndictation>]": [
            global_chrome_new_search,
            "lucky ",
            utils.text,
            " ",
        ],
    }
)
