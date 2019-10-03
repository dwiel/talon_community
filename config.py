import json
import os

from talon import resource

try:
    config = json.load(resource.open("config.json"))
except Exception:
    config = {}


def load_config_json(filename, default=dict):
    if not os.path.isfile(filename):
        with resource.open(filename, "w") as f:
            print('creating file', filename)
            f.write(json.dumps(default()))

    try:
        return json.load(resource.open(filename))
    except Exception as e:
        print(f"error opening {filename}: {e}")
        return default()


def save_config_json(filename, config):
    with resource.open(filename, "w") as f:
        f.write(json.dumps(config))
