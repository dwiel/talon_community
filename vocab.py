from talon.voice import Context

from . import config
from .text import shrink

vocab_alternate = config.load_config_json("vocab_alternate.json", dict)

vocab_alternate.update({f"shrink {k}": v for k, v in shrink.shrink_map.items()})

ctx = Context("vocab")
ctx.vocab = config.load_config_json("vocab.json", list) + list(vocab_alternate.keys())
ctx.vocab_remove = config.load_config_json("vocab_remove.json", list)
