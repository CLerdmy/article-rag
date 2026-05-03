import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"
_CONFIG_CACHE = None

def load_config():
    global _CONFIG_CACHE
    if _CONFIG_CACHE is None:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            _CONFIG_CACHE = json.load(file)
    return _CONFIG_CACHE