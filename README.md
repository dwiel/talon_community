[![CircleCI](https://circleci.com/gh/dwiel/talon_community/tree/master.svg?style=svg)](https://circleci.com/gh/dwiel/talon_community/tree/master)

# talon_community

A single source of application-specific scripts

Clone a fork of this repository in a directory inside of your `user` directory, such as `community`.

## Installation

If you wish to develop on these scripts, run in the project root:

```
python3 setup.py install
```

To install linters and formatter

## General Guidelines

- The `apps/` folder is "single script per app, named by the app", nothing goes in the apps folder unless it's a script supporting exactly one app with a context properly scoped to the app (unscoped scripts are fine for now for apps like spectacle, though probably note down the app's bundle identifier in the script so we can detect if it's running later)
- Context-specific languages (programming, spoken languages, specific config file syntax, that sort of thing) goes in `lang/`, generic text insertion goes in `text/`, anything else goes in `misc/`
- Try to not duplicate existing commands/functionality. There should only be one way to do something and typically only one way to say something (symbols/operators are a notable exception).
- If you're renaming/refactoring: the "one command" for an action should also be named to be clear about what it's doing, and err on the side of slightly verbose, ideally prefixed with a mental context. This is because it's easier for users to bolt shortcuts onto an expressive grammar than learn a non-composable compact grammar like voicecode. An example of this is `tab close` is more expressive than `totch` and is prefixed with the `tab` scope. voicecode's grammar can be bolted on later / as a separate set of scripts. "voicecode compatibility" is something of an opposite goal to coming up with a consistent grammar.
- use relative imports
- spaces for indentation
- follow `ctx = Context()`, `ctx.keymap({})` instead of using a separate dict unless you have a good reason

## Context activation

When adding new commands, try to scope their context as narrowly as possible.

The implementation of a flexible way to determine context activtion is a work in progress. For the time being:

- For commands that apply to a number of bundles, use the bundle groups defined in bundle_groups.py
- For commands that apply to specific file types, use the `is_filetype` helper in utils.py. This helper relies on the file type appearing in the window title. If you wish to use file type specific commands in an application that does not display the file type in the window title, either remove that application's bundle id from the file type sensitive bundles group, or add something that will match the window title to the list of file types for that context.

## Gotchas

- Some users may need to change the , mapping from `"comma": ","` to `",": ","`.
- Context names cannot have spaces
- If your output is missing the odd random letter, try [patching Talon's default delay](https://talonvoice.slack.com/archives/C9MBPTXD4/p1550012706021300)
- Refactoring is in progress and currently some commands in global contexts clash with others

## Script-specific notes

- `speech_toggle.py`: Note the 'dictation mode', which behaves similarly to dragon mode, but keeps Talon in control. It is a workaround for the inability of Dragon in 'dragon mode' to maintain focus on the front most application in some situations.
- `keeper.py`: The `phrase` command will only preserve literally the first part of the utterance. Anything that might be a command after the first word will be interpreted as such. `keeper` tries to preserve everything.

## Rules of precedence

The following have been empirically determined, could change at any point, and are not to be relied on:

 - Given two definitions for "foo" in the same keymap, the second will be used.
 - Given definitions for, 1. "foo <dgngdictation>"  2. "foo" and 3. "bar", saying "foo bar" will trigger (2) then (3) and saying "foo baz" will trigger (1).

