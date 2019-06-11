from talon.voice import Context, Key

from ..utils import text

PREFIX = "jet "

# Note that there are no application or window filters on this context because
# git may need to be used outside of the terminal, such as in a browser
# terminal, or you may need to send git commands to your friends to help them
# out with their git troubles.
ctx = Context("git")

ctx.keymap(
    {
        # TODO: remove duplication between the two groups of commands as we really
        # only need one set of commands (eg by completing github issue #40 (use a
        # more comprehensive git grammar))
        # git commands originally from std.py
        # git commands originally from terminal.py
        # PREFIX + "[<dgndictation>]": ["git ", text],
        PREFIX + "add [<dgndictation>]": ["git add ", text],
        PREFIX + "add partial [<dgndictation>]": ["git add -p ", text],
        PREFIX + "bisect": "git bisect ",
        PREFIX + "branch": "git branch ",
        PREFIX
        + "branch set up stream to [<dgndictation>]": [
            "git branch --set-upstream-to=",
            text,
        ],
        PREFIX + "branch delete [<dgndictation>]": ["git branch -D ", text],
        PREFIX + "branch all [<dgndictation>]": ["git branch -a ", text],
        PREFIX + "clone [<dgndictation>]": ["git clone ", text],
        PREFIX + "checkout master": "git checkout master",
        PREFIX + "checkout [<dgndictation>]": ["git checkout ", text],
        PREFIX + "checkout branch [<dgndictation>]": ["git checkout -B ", text],
        PREFIX + "cherry pick [<dgndictation>]": ["git cherry-pick ", text],
        PREFIX + "commit [<dgndictation>]": ['git commit -m ""', Key("left"), text],
        PREFIX
        + "commit amend [<dgndictation>]": [
            'git commit --amend -m ""',
            Key("left"),
            text,
        ],
        PREFIX
        + "commit all [<dgndictation>]": ['git commit -a -m ""', Key("left"), text],
        PREFIX
        + "commit ticket [number]": ['git commit -m "[#]"', Key("left"), Key("left")],
        PREFIX + "config [<dgndictation>]": ["git config ", text],
        PREFIX + "config list [<dgndictation>]": ["git config --list ", text],
        PREFIX + "diff [<dgndictation>]": ["git diff ", text],
        PREFIX + "diff staged": "git diff --staged ",
        PREFIX + "fetch": "git fetch ",
        PREFIX + "history": "git hist ",
        PREFIX + "grep": "git grep ",
        PREFIX + "(in it | init | initialize)": "git init ",
        PREFIX + "log": "git log ",
        PREFIX + "merge [<dgndictation>]": ["git merge ", text],
        PREFIX + "move [<dgndictation>]": ["git mv ", text],
        PREFIX + "pull [<dgndictation>]": ["git pull ", text],
        PREFIX
        + "pull (base | re-base | rebase | re base) [<dgndictation>]": [
            "git pull --rebase ",
            text,
        ],
        PREFIX + "push [<dgndictation>]": ["git push ", text],
        PREFIX + "push force [<dgndictation>]": ["git push --force ", text],
        PREFIX
        + "push force lease [<dgndictation>]": ["git push --force-with-lease ", text],
        PREFIX
        + "push set up stream [<dgndictation>]": ["git push --set-upstream ", text],
        PREFIX + "push set up new branch": "git push --set-upstream origin HEAD",
        PREFIX + "rebase continue": "git rebase --continue",
        PREFIX + "rebase [<dgndictation>]": ["git rebase ", text],
        PREFIX + "remote add [<dgndictation>]": ["git remote add ", text],
        PREFIX + "(remove | R M) [<dgndictation>]": ["git rm ", text],
        PREFIX + "reset [<dgndictation>]": ["git reset ", text],
        PREFIX + "reset hard": "git reset --hard ",
        PREFIX + "revert [<dgndictation>]": ["git revert ", text],
        PREFIX + "show": "git show ",
        PREFIX + "stash": "git stash ",
        PREFIX + "stash apply": "git stash apply ",
        PREFIX + "stash pop": "git stash pop ",
        PREFIX + "status": "git status ",
        PREFIX + "submodule": "git submodule ",
        PREFIX + "submodule add": "git submodule add ",
        PREFIX + "submodule in it": "git submodule init",
        PREFIX + "submodule update": "git submodule update",
        PREFIX + "tag": "git tag ",
        PREFIX + "add commit": ["git add  && git commit"] + ([Key("left")] * 14),
    }
)
