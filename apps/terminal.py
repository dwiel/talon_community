from talon.voice import Word, Key, Context, Str, press
import string

from ..utils import numerals, parse_words

terminals = ('com.apple.Terminal', 'com.googlecode.iterm2')
ctx = Context('terminal', func=lambda app, win: any(
    t in app.bundle for t in terminals))

mapping = {
    'semicolon': ';',
    r'new-line': '\n',
    r'new-paragraph': '\n\n',
}

def parse_word(word):
    word = word.lstrip('\\').split('\\', 1)[0]
    word = mapping.get(word, word)
    return word

# Ask for forgiveness not permission in failure scenario.
# https://stackoverflow.com/questions/610883/how-to-know-if-an-object-has-an-attribute-in-python
def text(m):
    try:
        tmp = [str(s).lower() for s in m.dgndictation[0]._words]
        words = [parse_word(word) for word in tmp]
        Str(' '.join(words))(None)
    except AttributeError:
        return


def dash(m):
    words = parse_words(m)
    press(' ')
    if len(words) == 1 and len(words[0]) == 1:
        press('-')
        Str(words[0])(None)
    else:
        press('-')
        press('-')
        Str('-'.join(words))(None)


keymap = {
    # some habits die hard
    'troll char': Key('ctrl-c'),
    'reverse': Key('ctrl-r'),

    'cd': ['cd ; ls', Key('left'), Key('left'), Key('left'), Key('left')],
    'cd wild': ['cd **; ls', Key('left'), Key('left'), Key('left'), Key('left'), Key('left')],
    'cd wild [<dgndictation>]': ['cd **; ls', Key('left'), Key('left'), Key('left'), Key('left'), Key('left'), text],
    '(ls | run ellis | run alice)': 'ls\n',
    '(la | run la)': 'ls -la\n',
    'durrup': 'cd ..; ls\n',
    'go back': 'cd -\n',

    'dash <dgndictation> [over]': dash,

    'pseudo': 'sudo ',
    'shell clear': [Key('ctrl-c'), 'clear\n'],
    'shell copy [<dgndictation>]': ['cp ', text],
    'shell copy (recursive | curse) [<dgndictation>]': ['cp -r', text],
    'shell kill': Key('ctrl-c'),
    'shell list [<dgndictation>]': ['ls ', text],
    'shell list all [<dgndictation>]': ['ls -la ', text],
    'shell make (durr | dear) [<dgndictation>]': ['mkdir ', text],
    'shell mipple [<dgndictation>]': ['mkdir -p ', text],
    'shell move [<dgndictation>]': ['mv ', text],
    'shell remove [<dgndictation>]': ['rm ', text],
    'shell remove (recursive | curse) [<dgndictation>]': ['rm -rf ', text],
    "shell enter": "ag -l | entr ",
    "shell enter 1": "ag -l . .. | entr ",
    "shell enter 2": "ag -l . ../.. | entr ",
    'shell less [<dgndictation>]': ['less ', text],
    'shell cat [<dgndictation>]': ['cat ', text],
    'shell X args [<dgndictation>]': ['xargs ', text],
    'shell mosh': 'mosh ',
    'shell M player': 'mplayer ',
    'shell nvidia S M I': 'nvidia-smi ',

    'create virtual environment': ['virtualenv -p python3 venv', Key('enter')],
    'activate virtual environment': ['source `find . | grep bin/activate$`', Key('enter')],

    'apt get': 'apt-get ',
    'apt get install': 'apt-get install ',
    'apt get update': 'apt-get update ',
    'apt get upgrade': 'apt-get upgrade ',

    # git
    'jet [<dgndictation>]': ['git ', text],
    'jet add [<dgndictation>]': ['git add ', text],
    'jet branch': 'git branch',
    'jet branch delete [<dgndictation>]': ['git branch -D ', text],
    'jet branch all [<dgndictation>]': ['git branch -a ', text],
    'jet clone [<dgndictation>]': ['git clone ', text],
    'jet checkout master': 'git checkout master\n',
    'jet checkout [<dgndictation>]': ['git checkout ', text],
    'jet checkout branch [<dgndictation>]': ['git checkout -B ', text],
    'jet commit [<dgndictation>]': ['git commit -m ""', Key('left'), text],
    'jet commit amend [<dgndictation>]': ['git commit --amend -m ""', Key('left'), text],
    'jet commit all [<dgndictation>]': ['git commit -a -m ""', Key('left'), text],
    'jet diff [<dgndictation>]': ['git diff ', text],
    'jet history': 'git hist\n',
    'jet merge [<dgndictation>]': ['git merge ', text],
    'jet move [<dgndictation>]': ['git mv ', text],
    'jet pull [<dgndictation>]': ['git pull ', text],
    'jet pull (base | re-base) [<dgndictation>]': ['git pull --rebase ', text],
    'jet push [<dgndictation>]': ['git push ', text],
    'jet push force [<dgndictation>]': ['git push --force', text],
    'jet rebase [<dgndictation>]': ['git rebase ', text],
    'jet remove [<dgndictation>]': ['git rm ', text],
    'jet reset': 'git reset\n',
    'jet reset hard': 'git reset --hard\n',
    'jet show': 'git show ',
    'jet stash': 'git stash',
    'jet stash apply': 'git stash apply',
    'jet status': 'git status',

    # Tools
    '(grep | grip)': ['grep  .', Key('left left')],
    'gripper': ['grep -r  .', Key('left left')],
    'pee socks': 'ps aux ',
    'vi': 'vi ',

    # python
    'pip': 'pip',
    'pip install': 'pip install ',
    'pip install requirements': 'pip install -r ',
    'pip install editable': 'pip install -e ',
    'pip install this': 'pip install -e .',
    'pip install upgrade': 'pip install --upgrade ',
    'pip uninstall': 'pip uninstall ',
    'pip list': 'pip list',

    # kubectl
    'cube control': 'kubectl ',
    'cube create': 'kubectl create ',
    'cube expose': 'kubectl expose ',
    'cube run': 'kubectl run ',
    'cube set': 'kubectl set ',
    'cube run-container': 'kubectl run-container ',
    'cube get': 'kubectl get ',
    'cube get nodes': 'kubectl get nodes',
    'cube get jobs': 'kubectl get jobs',
    'cube get pods': 'kubectl get pods',
    'cube explain': 'kubectl explain ',
    'cube edit': 'kubectl edit ',
    'cube delete': 'kubectl delete ',
    'cube rollout': 'kubectl rollout ',
    'cube rolling-update': 'kubectl rolling-update ',
    'cube scale': 'kubectl scale ',
    'cube autoscale': 'kubectl autoscale ',
    'cube certificate': 'kubectl certificate ',
    'cube cluster-info': 'kubectl cluster-info ',
    'cube top': 'kubectl top ',
    'cube cordon': 'kubectl cordon ',
    'cube uncordon': 'kubectl uncordon ',
    'cube drain': 'kubectl drain ',
    'cube taint': 'kubectl taint ',
    'cube describe': 'kubectl describe ',
    'cube logs': 'kubectl logs ',
    'cube attach': 'kubectl attach ',
    'cube exec': 'kubectl exec ',
    'cube port-forward': 'kubectl port-forward ',
    'cube proxy': 'kubectl proxy ',
    'cube cp': 'kubectl cp ',
    'cube auth': 'kubectl auth ',
    'cube apply': 'kubectl apply ',
    'cube patch': 'kubectl patch ',
    'cube replace': 'kubectl replace ',
    'cube convert': 'kubectl convert ',
    'cube label': 'kubectl label ',
    'cube annotate': 'kubectl annotate ',
    'cube completion': 'kubectl completion ',
    'cube api': 'kubectl api ',
    'cube config': 'kubectl config ',
    'cube help': 'kubectl help ',
    'cube plugin': 'kubectl plugin ',
    'cube version': 'kubectl version ',
}

keymap.update({'pain '+str(i): Key('alt-'+str(i)) for i in range(10)})

ctx.keymap(keymap)


# module.exports = {
#   permissions: "chmod "
#   access: "chmod "
#   ownership: "chown "
#   "change own": "chown "
#   "change group": "chgrp "
#   cat: "cat "
#   chat: "cat " # dragon doesn't like the word 'cat'
#   copy: "cp "
#   "copy recursive": "cp -r "
#   move: "mv "
#   remove: "rm "
#   "remove recursive": "rm -rf "
#   "remove directory": "rmdir "
#   "make directory": "mkdir "
#   link: "ln "
#   man: "man "
#   list: "ls "
#   "list all": "ls -al "
#   ls: "ls "
#
#   "python reformat": "yapf -i "
#   "enter": "ag -l | entr "
#   "enter to": "ag -l . ../.. | entr "
# }
