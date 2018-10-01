# talon_community
A single source of application-specific scripts

Clone a fork of this repository in a directory inside of your `user` directory, such as `community`.

## General Guidelines

- The `apps/` folder is "single script per app, named by the app", nothing goes in the apps folder unless it's a script supporting exactly one app with a context properly scoped to the app (unscoped scripts are fine for now for apps like spectacle, though probably note down the app's bundle identifier in the script so we can detect if it's running later)
- Context-specific languages (programming, spoken languages, specific config file syntax, that sort of thing) goes in `lang/`, generic text insertion goes in `text/`, anything else goes in `misc/`
- Try to not duplicate existing commands/functionality. There should only be one way to do something and typically only one way to say something (symbols/operators are a notable exception).
- If you're renaming/refactoring: the "one command" for an action should also be named to be clear about what it's doing, and err on the side of slightly verbose, ideally prefixed with a mental context. This is because it's easier for users to bolt shortcuts onto an expressive grammar than learn a non-composable compact grammar like voicecode. An example of this is `tab close` is more expressive than `totch` and is prefixed with the `tab` scope. voicecode's grammar can be bolted on later / as a separate set of scripts. "voicecode compatibility" is something of an opposite goal to coming up with a consistent grammar.
- use relative imports
- spaces for indentation
- follow `ctx = Context()`, `ctx.keymap({})` instead of using a separate dict unless you have a good reason
