import json
from pathlib import Path

REGISTRY_DIR = Path.home() / ".stash"
REGISTRY_FILE = REGISTRY_DIR / "projects.json"


def load_projects() -> dict:
    if not REGISTRY_FILE.exists():
        return {"projects":{}}
    
    with REGISTRY_FILE.open("r",encoding="utf-8") as file:
        return json.load(file)
    
    
def save_projects(data:dict)->None:
    REGISTRY_DIR.mkdir(parents=True,exist_ok=True)
    
    with REGISTRY_FILE.open("w",encoding="utf-8") as file:
        json.dump(data,file,indent=4)
        

def register_project(name:str,path:Path)->None:
    data = load_projects()
    
    path = path.resolve()
    
    if not path.is_dir():
        raise ValueError(f"Project directory does not exist: {path}")
    
    if name in data["projects"]:
        raise ValueError(f"Project '{name}' is already registered.")

    data["projects"][name]={
        "path":str(path)
    }
    
    save_projects(data)


def unregister_project(name: str) -> None:
    data = load_projects()

    if name not in data["projects"]:
        raise ValueError(
            f"Project '{name}' is not registered."
        )

    del data["projects"][name]

    save_projects(data)
