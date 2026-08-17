import json
from pathlib import Path

def save_json(data, filename):

    with open(filename, "w") as f:
        json.dump(data, f)


def load_json(filename):

    with open(filename) as f:
        return json.load(f)