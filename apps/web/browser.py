import time
from decorator import decorator

from talon.voice import press, Key

from ...utils import insert

lag = 0.2
using_tridactyl = False
using_vimium = True


def normal_mode():
    # get out of any text box
    time.sleep(lag)
    press("escape")
    press("escape")
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
    elif using_vimium:
        press("escape")
        press("escape")
        press("i")


def do(thing, *args, **kwargs):
    if isinstance(thing, str):
        insert(thing)
    elif isinstance(thing, (Key)):
        thing(args[0])
    elif isinstance(thing, (list, tuple)):
        for element in thing:
            do(element)
    else:
        thing(*args, **kwargs)


@decorator
def send_to_page(function=None, stay_in_page_mode=False):
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
