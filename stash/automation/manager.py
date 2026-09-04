import json
from pathlib import Path

def load_automation(path:Path) -> dict:
    with path.open('r') as file:
        return json.load(file)
    


automation = load_automation(Path("automations/python.json"))


