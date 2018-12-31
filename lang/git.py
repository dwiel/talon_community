from talon.voice import Context, Key

from ..utils import text

# Note that there are no application or window filters on this context because
# git may need to be used outside of the terminal, such as in a browser
# terminal, or you may need to send git commands to your friends to help them
# out with their git troubles.
ctx = Context("git")

ctx.keymap({
    # TODO: remove duplication between the two groups of commands as we really
    # only need one set of commands (eg by completing github issue #40 (use a
    # more comprehensive git grammar))

    # git commands originally from std.py
    "run get": "git ",
    "run get (R M | remove)": "git rm ",
    "run get add": "git add ",
    "run get bisect": "git bisect ",
    "run get branch": "git branch ",
    "run get checkout": "git checkout ",
    "run get clone": "git clone ",
    "run get commit": "git commit ",
    "run get diff": "git diff ",
    "run get fetch": "git fetch ",
    "run get grep": "git grep ",
    "run get in it": "git init ",
    "run get log": "git log ",
    "run get merge": "git merge ",
    "run get move": "git mv ",
    "run get pull": "git pull ",
    "run get push": "git push ",
    "run get rebase": "git rebase ",
    "run get reset": "git reset ",
    "run get show": "git show ",
    "run get status": "git status ",
    "run get tag": "git tag ",

    # git commands originally from terminal.py
    "jet [<dgndictation>]": ["git ", text],
    "jet add [<dgndictation>]": ["git add ", text],
    "jet branch": "git branch",
    "jet branch delete [<dgndictation>]": ["git branch -D ", text],
    "jet branch all [<dgndictation>]": ["git branch -a ", text],
    "jet clone [<dgndictation>]": ["git clone ", text],
    "jet checkout master": "git checkout master",
    "jet checkout [<dgndictation>]": ["git checkout ", text],
    "jet checkout branch [<dgndictation>]": ["git checkout -B ", text],
    "jet cherry pick [<dgndictation>]": ["git cherry-pick ", text],
    "jet commit [<dgndictation>]": ['git commit -m ""', Key("left"), text],
    "jet commit amend [<dgndictation>]": [
        'git commit --amend -m ""',
        Key("left"),
        text,
    ],
    "jet commit all [<dgndictation>]": [
        'git commit -a -m ""',
        Key("left"),
        text,
    ],
    "jet config [<dgndictation>]": ["git config ", text],
    "jet config list [<dgndictation>]": ["git config --list ", text],
    "jet diff [<dgndictation>]": ["git diff ", text],
    "jet history": "git hist ",
    "jet (init | initialize)": "git init ",
    "jet log": "git log ",
    "jet merge [<dgndictation>]": ["git merge ", text],
    "jet move [<dgndictation>]": ["git mv ", text],
    "jet pull [<dgndictation>]": ["git pull ", text],
    "jet pull (base | re-base | rebase | re base) [<dgndictation>]": [
        "git pull --rebase ",
        text,
    ],
    "jet push [<dgndictation>]": ["git push ", text],
    "jet push force [<dgndictation>]": ["git push --force ", text],
    "jet push set up stream [<dgndictation>]": [
        "git push --set-upstream ",
        text,
    ],
    "jet rebase continue": "git rebase --continue",
    "jet rebase [<dgndictation>]": ["git rebase ", text],
    "jet remove [<dgndictation>]": ["git rm ", text],
    "jet reset": "git reset ",
    "jet reset hard": "git reset --hard ",
    "jet show": "git show ",
    "jet stash": "git stash ",
    "jet stash apply": "git stash apply ",
    "jet stash pop": "git stash pop ",
    "jet status": "git status ",
})
