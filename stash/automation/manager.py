
import json
from pathlib import Path


def load_automation(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
