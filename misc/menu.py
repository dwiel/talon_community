from talon import applescript, ui
from talon.voice import Context

from user.misc.std import parse_words

ctx = Context('menu')

menu_items = {}


def select_menu_bar_item(m):
    name = str(m._words[1])
    full = menu_items.get(name)
    if not full:
        return
    applescript.run(r'''
tell application "System Events"
  tell (first process whose frontmost is true)
    click menu bar item "%s" of menu bar 1
  end tell
end tell
    ''' % full)


def update_lists():
    global menu_items
    items = applescript.run(r'''
on menubar_items()
    tell application "System Events"
        tell (first process whose frontmost is true)
            tell menu bar 1
                set test to name of every menu bar item
                return test
            end tell
        end tell
    end tell
end menubar_items

set theList to menubar_items()
set {text item delimiters, TID} to {",", text item delimiters}
set {text item delimiters, theListAsString} to {TID, theList as text}
return theListAsString
''')
    items = items.split(',')
    new = {}
    for item in items:
        words = item.split(' ')
        for word in words:
            if word and not word in new:
                new[word] = item
        new[item] = item
    if set(new.keys()) == set(menu_items.keys()):
        return
    ctx.set_list('menu_items', new.keys())
    menu_items = new
    print(('menu_items', menu_items))


def ui_event(event, arg):
    if event in ('app_activate', 'app_launch', 'app_close', 'win_open',
                 'win_close'):
        update_lists()


ui.register('', ui_event)
update_lists()

keymap = {
    'menu {menu.menu_items}': select_menu_bar_item,
}
ctx.keymap(keymap)
