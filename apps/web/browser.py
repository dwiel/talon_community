import time
import re

from talon.voice import press, Key
from talon import ui

from ...utils import insert
from ... import utils

lag = 0.2
using_tridactyl = False
using_vimium = True
using_surfingkeys = False
BROWSERS = ["com.google.Chrome", "org.mozilla.firefox"]

cache_times = {}
cache_values = {}


def get_url(win=None):
    if win is None:
        win = ui.active_window()

    now = time.time()
    last_cache = cache_times.get(win, default=0)
    if now - last_cache > .1:
        url = _get_url(win)
        cache_values[win] = url
        cache_times[win] = time.time()

    # print(now - last_cache, now, last_cache, cache_values[win])
    return cache_values[win]


def _get_url(win=None):
    if win.app.bundle == "com.google.Chrome":
        children = win.children.find(AXRole="AXTextField")
        try:
            return children[0].AXValue
        except IndexError as e:
            return ""
        # return win.children.find(AXTitle="Address and search bar")[0].AXValue
    else:
        raise ValueError("no method for getting url from not chrome yet")
    # win.children.find(AXTitle='Address and search bar')[0].AXValue


def set_url(url, win=None):
    if win is None:
        win = ui.active_window()
    focus_address_bar()
    utils.paste_text(url)


def navigate_to_url(url, win=None):
    set_url(url, win)
    press("enter")


def url_matches_func(url_pattern):
    if url_pattern[:8] == "https://":
        url_pattern = "(https://)?" + url_pattern[8:]
    elif url_pattern[:7] == "http://":
        url_pattern = "(http://)?" + url_pattern[7:]
    else:
        url_pattern = "(http://|https://)?" + url_pattern

    def func(app, win):
        if win.app.bundle == "com.google.Chrome":
            result = bool(re.fullmatch(url_pattern, get_url(win)))
            # if result:
            # print("matches", result, url_pattern, type(get_url(win)), repr(get_url(win)))
            return result

        else:
            return False

    return func


def focus_address_bar(m=None):
    press("cmd-l")


def normal_mode():
    focus_address_bar(None)
    time.sleep(0.1)
    press("escape")
    press("escape")
    # time.sleep(0.1)
    # This leaves the focus on the page at previous tab focused point, not the beginning of the page
    press("tab")

    # # get out of any text box
    # time.sleep(lag)
    # press("escape")
    # press("escape")
    # time.sleep(lag)


def tridactyl_mode():
    if using_tridactyl:
        # normal_mode()
        time.sleep(lag)
        press("ctrl-alt-escape")
        time.sleep(lag)
    else:
        press("escape")


def page_mode():
    normal_mode()
    if using_tridactyl:
        press("ctrl-alt-escape")
        time.sleep(lag)
    elif using_vimium:
        # google sheets can't handle multiple escapes here.
        press("escape")
        time.sleep(lag)
        press("i")
    elif using_surfingkeys:
        print("after normal")
        press("alt-i")
        time.sleep(lag)


def do(thing, *args, **kwargs):
    if isinstance(thing, str):
        insert(thing)
    elif isinstance(thing, Key):
        thing(args[0])
    elif isinstance(thing, (list, tuple)):
        for element in thing:
            do(element)
    else:
        thing(*args, **kwargs)


# @decorator
def send_to_page(function=None, stay_in_page_mode=False):
    # @send_to_page(stay_in_page_mode=foo)
    if function is None:

        def wrapper_wrapper(function):
            def wrapper(*args, **kwargs):
                page_mode()
                do(function, *args, **kwargs)
                if not stay_in_page_mode:
                    tridactyl_mode()

            return wrapper

        return wrapper_wrapper
    # @send_to_page or send_to_page(Key('a'), ...)
    else:

        def wrapper(*args, **kwargs):
            page_mode()
            do(function, *args, **kwargs)
            if not stay_in_page_mode:
                tridactyl_mode()

        return wrapper


# @decorator
def send_to_vimium(function=None):
    def wrapper(*args, **kwargs):
        normal_mode()
        print(function, *args, **kwargs)
        do(function, *args, **kwargs)

    return wrapper


# "hello world": send_to_page(Key('h'))
