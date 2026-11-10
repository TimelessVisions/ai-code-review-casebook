import json


def load_config(path: str) -> dict:
    """Load JSON config; a missing file means 'no config'."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
