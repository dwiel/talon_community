"""
Commands for RStudio <https://www.rstudio.com/>

Note that the Preview release of RStudio often has additional keyboard
shortcuts over the Stable release:
<https://www.rstudio.com/products/rstudio/download/preview/>
Compatible with RStudio Preview >= v1.2.1578.

Also see `r-lang.py` at <https://github.com/seananderson/talon-config>, which
has commands for some common Tidyverse R functions.
"""

from talon.voice import Context, Key

ctx = Context("RStudio", bundle="org.rstudio.RStudio")

ctx.keymap(
    {
        # The shortcut to rule them all
        "show keyboard shortcuts": Key("alt-shift-k"),
        #
        # Running code
        "run that": Key("cmd-enter"),
        "run previous": Key("cmd-shift-p"),
        "run document": Key("cmd-alt-r"),
        "run from top": Key("cmd-alt-b"),
        "run to end": Key("cmd-alt-e"),
        "run (function|funk)": Key("cmd-alt-f"),
        "run section": Key("cmd-alt-t"),
        "run previous chunks": Key("cmd-alt-p"),
        "run chunk": Key("cmd-alt-c"),
        "run next chunk": Key("cmd-alt-n"),
        "run all": Key("cmd-shift-s"),
        "run knitter": Key("cmd-shift-k"),
        "run profiler": Key("cmd-shift-alt-p"),
        #
        # Moving around and formatting
        "jump back": Key("cmd-f9"),
        "jump forward": Key("cmd-f10"),
        "close all tabs": Key("cmd-shift-w"),
        "indent lines": Key("cmd-i"),
        "toggle comment": Key("cmd-shift-c"),
        "reformat comment": Key("cmd-shift-/"),
        "reformat R code": Key("cmd-shift-a"),
        "line up": Key("alt-up"),
        "line down": Key("alt-down"),
        "duplicate line up": Key("cmd-alt-up"),
        "duplicate line [down]": Key("cmd-alt-down"),
        "select to paren": Key("ctrl-shift-e"),
        "select to matching paren": Key("ctrl-shift-alt-e"),
        "jump to matching": Key("ctrl-p"),
        "expand selection": Key("shift-alt-cmd-up"),
        "reduce selection": Key("shift-alt-cmd-down"),
        "add cursor up": Key("ctrl-alt-up"),
        "add cursor down": Key("ctrl-alt-down"),
        "move active cursor up": Key("ctrl-alt-shift-up"),
        "move active cursor down": Key("ctrl-alt-shift-down"),
        "delete line": Key("cmd-d"),
        "delete word left": Key("alt-backspace"),
        "delete word right": Key("alt-delete"),
        "assign that": Key("alt--"),
        "pipe that": Key("cmd-shift-m"),
        "insert knitter chunk": Key("cmd-alt-i"),
        #
        # Folding
        "fold that": Key("cmd-alt-l"),
        "unfold that": Key("cmd-shift-alt-l"),
        "fold all": Key("cmd-alt-o"),
        "unfold all": Key("cmd-shift-alt-o"),
        #
        # Find and replace
        "find and replace": Key("cmd-f"),
        "find next": Key("cmd-g"),
        "find previous": Key("cmd-shift-g"),
        "find with selection": Key("cmd-e"),
        "find in files": Key("cmd-shift-f"),
        "run replace": Key("cmd-shift-j"),
        "run spell check": Key("f7"),
        #
        # Navigation and panels
        "go to source": Key("ctrl-1"),
        "go to console": Key("ctrl-2"),
        "go to help": Key("ctrl-3"),
        "go to history": Key("ctrl-4"),
        "go to files": Key("ctrl-5"),
        "go to (plots|plot)": Key("ctrl-6"),
        "go to packages": Key("ctrl-7"),
        "go to environment": Key("ctrl-8"),
        "go to git": Key("ctrl-9"),
        "go to build": Key("ctrl-0"),
        "go to terminal": Key("alt-shift-t"),
        "go to omni": Key("ctrl-."),
        "go to line": Key("cmd-shift-alt-g"),
        "go to section": Key("cmd-shift-alt-j"),
        "go to tab": Key("ctrl-shift-."),
        "go to previous tab": Key("ctrl-f11"),
        "go to next tab": Key("ctrl-f12"),
        "go to first tab": Key("ctrl-shift-f11"),
        "go to last tab": Key("ctrl-shift-f12"),
        "zoom source": Key("ctrl-shift-1"),
        "(zoom|show) all panes": Key("ctrl-shift-0"),
        "help that": Key("f1"),
        "define that": Key("f2"),
        "previous plot": Key("cmd-alt-f11"),
        "next plot": Key("cmd-alt-f12"),
        #
        # devtools, package development, and session management
        "restart R session": Key("cmd-shift-f10"),
        "dev tools build": Key("cmd-shift-b"),
        "dev tools load all": Key("cmd-shift-l"),
        "dev tools test": Key("cmd-shift-t"),
        "dev tools check": Key("cmd-shift-e"),
        "dev tools document": Key("cmd-shift-d"),
        #
        # Debugging
        "toggle breakpoint": Key("shift-f9"),
        "debug next": Key("f10"),
        "debug step into (function|funk)": Key("shift-f4"),
        "debug finish (function|funk)": Key("shift-f6"),
        "debug continue": Key("shift-f5"),
        "debug stop": Key("shift-f8"),
        #
        # Git/SVN
        "run git diff": Key("ctrl-alt-d"),
        "run git commit": Key("ctrl-alt-m"),
        #
        # Other shortcuts that could be enabled
        # "run line and stay": Key("alt-enter"),
        # "run and echo all": Key("cmd-shift-enter"),
        # "extract (function|funk)": Key("cmd-alt-x"),
        # "extract variable": Key("cmd-alt-v"),
        # "new terminal": Key("shift-alt-t"),
        # "rename current terminal": Key("shift-alt-r"),
        # "clear current terminal": Key("ctrl-shift-l"),
        # "previous terminal": Key("ctrl-alt-f11"),
        # "next terminal": Key("ctrl-alt-f12"),
        # "clear console": Key("ctrl-l"),
        # "popup history": Key("cmd-up"),
        # "change working directory": Key("ctrl-shift-h"),
        # "new document": Key("cmd-shift-n"),
        # "new document chrome": Key("cmd-shift-alt-n"),
        # "insert code section": Key("cmd-shift-r"),
        # "scroll diff view": Key("ctrl-up/down"),
        # "sync editor and pdf preview": Key("cmd-f8"),
    }
)
