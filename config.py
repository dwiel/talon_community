import json

from talon import resource

try:
    config = json.load(resource.open("config.json"))
except Exception:
    config = {}
