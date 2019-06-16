import json
import os

from talon import resource

try:
    config = json.load(resource.open("config.json"))
except Exception:
    config = {}


def load_config_json(filename, default=dict):
    if not os.path.isfile(filename):
        with open(filename, "w") as f:
            f.write("{}")

    try:
        return json.load(resource.open(filename))
    except Exception as e:
        print(f"error opening {filename}: {e}")
        return default()
