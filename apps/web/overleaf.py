from talon.voice import Context, Key, press, Str

from . import browser
from ... import utils

BROWSERS = ["com.google.Chrome", "org.mozilla.firefox"]
ctx = Context("overleaf", func=browser.url_matches_func("https://www.overleaf.com/.*"))


def go_to_line(m):
    line = utils.extract_num_from_m(m, default=None)
    print(line)

    press("cmd-l")
    Str(str(line))(None)
    press("enter")


ctx.keymap({"spring" + utils.numerals: go_to_line, "new line": "\\newline"})
