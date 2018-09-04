from talon.voice import Context, Key

ctx = Context('bit-bucket', func=lambda app, win: 'Bitbucket' in win.title)

keymap = {
    # All Pages
    'shortcuts': Key('?'),
    'left navigation': Key('['),
    'site search': Key('/'),

    # Most Pages (except your work and repository source)
    'omnibar': Key('.'),
    'next item': Key('j'),
    'last item': Key('k'),
    'selected': Key('o'),
    'dashboard': Key('g d'),
    'settings': Key('g a'),
    'remove focus': Key('esc'),
    'go back': Key('u'),
    'right navigation': Key(']'),

    # Repository source
    'focus': Key('f'),

    # Repository pages (except source)
    'create': Key('c r'),
    'import': Key('i r'),
    'source': Key('r s'),
    'view commits': Key('r c'),
    'view branches': Key('r b'),
    'pull requests': Key('r p'),
    'issues': Key('r i'),
    'wiki': Key('r w'),
    'downloads': Key('r d'),
    'repo settings': Key('r a'),
    'find file': Key('f'),

    # Repository pages (except source and settings)
    'fork': Key('x f'),
    'create branch': Key('x b'),
    'compare': Key('x c'),
    'create pull request': Key('x p'),
    'create issue': Key('x i'),

    # Pull Requests
    'submit comment': Key('ctrl+enter'),
    'inline comments': Key('t c'),
    'diff tab': Key('p d'),
    'commits tab': Key('p c'),
    'activity tab': Key('p a'),
    'show tasks': Key('shift-t'),

}

ctx.keymap(keymap)
