import time

from ..utils import parse_words_as_integer
from talon.voice import Context, Key, Str, press

ctx = Context("firefox", bundle="org.mozilla.firefox")

# NOTE: run: bind --mode=ignore <Esc> composite unfocus | mode ignore


def focus_address_bar(m=None):
    press("cmd-l")


# Return focus from the devtools to the page
def refocus_page(m=None):
    focus_address_bar()
    time.sleep(0.1)
    # Escape button
    # This leaves the focus on the page at previous tab focused point, not the beginning of the page
    press("tab")


def back(m):
    # refocus_page(None)
    # press("cmd-[")
    press("escape")
    press("cmd-left")
    # refocus_page(None)


def forward(m):
    # refocus_page(None)
    # press("cmd-]")
    press("escape")
    press("cmd-right")
    # refocus_page(None)


def command_line(command):
    def function(m):
        refocus_page()
        press("escape", wait=2000)
        press("escape", wait=2000)
        press("escape", wait=2000)
        time.sleep(0.1)
        press(":", wait=2000)
        time.sleep(0.1)
        for character in command:
            press(character, wait=2000)
        # Str(command)(None)
        time.sleep(0.25)
        press("enter", wait=2000)

    return function


ctx.keymap(
    {
        "(address bar | focus address | focus url | url)": focus_address_bar,
        "copy url": Key("escape y y"),
        "back[ward]": back,
        "forward": forward,
        "reload": Key("cmd-r"),
        "hard reload": Key("cmd-shift-r"),
        "(last | prevous)": Key("cmd-shift-g"),
        "toggle dev tools": Key("cmd-alt-i"),
        "command menu": Key("cmd-shift-p"),
        "(reopen | unclose) tab": Key("cmd-shift-t"),
        # "next panel": next_panel,
        # "(last | prevous) panel": last_panel,
        # "show application [panel]": lambda m: show_panel("Application"),
        # "show audit[s] [panel]": lambda m: show_panel("Audits"),
        # "show console [panel]": lambda m: show_panel("Console"),
        # "show element[s] [panel]": lambda m: show_panel("Elements"),
        # "show memory [panel]": lambda m: show_panel("Memory"),
        # "show network [panel]": lambda m: show_panel("Network"),
        # "show performance [panel]": lambda m: show_panel("Performance"),
        # "show security [panel]": lambda m: show_panel("Security"),
        # "show source[s] [panel]": lambda m: show_panel("Sources"),
        "(refocus | focus) page": refocus_page,
        # "[refocus] dev tools": open_focus_devtools,
        # Clipboard
        # "cut": Key("cmd-x"),
        # "copy": Key("cmd-c"),
        # "paste": Key("cmd-v"),
        "paste same style": Key("cmd-alt-shift-v"),
        # extensions
        "mendeley": Key("cmd-shift-m"),
        # TODO: this should probably bem specific to the page
        "submit": Key("cmd-enter"),
        # t
        "switch mode": Key("ctrl-alt-escape"),
        # tridactyl
        "new personal tab": command_line("tabopen -c personal"),
        "(switch to personal [container] | personal container)": command_line(
            "composite get_current_url | tabopen -c personal"
        ),
        "show add-ons": Key("cmd-shift-a"),
    }
)
