from talon.voice import Context, Key


context = Context('lastpass', bundle='com.google.Chrome')

context.keymap({
    'last pass next': Key('cmd-pageup'),
    'last pass (previous | preev)': Key('cmd-pagedown'),
})
