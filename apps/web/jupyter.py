"""
https://github.com/jupyter/notebook/issues/3400

%%javascript
var cell = Jupyter.notebook.get_selected_cell();
var config = cell.config;
var patch = {
      CodeCell:{
        cm_config:{lineWiseCopyCut:false}
      }
    }
config.update(patch)

https://stackoverflow.com/questions/22843891/turn-off-auto-closing-parentheses-in-ipython/

from notebook.services.config import ConfigManager
c = ConfigManager()
c.update('notebook', {"CodeCell": {"cm_config": {"autoCloseBrackets": False}}})
"""


from talon.voice import Context, Key

ctx = Context("jupyter")

ctx.keymap({"cell run": Key("shift-enter")})
# command pallet
# restart and run all
# other?
