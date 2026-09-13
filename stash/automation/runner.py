from pathlib import Path
import subprocess



def create_folders(base_path:Path, folders: list[str]):
    for folder in folders:
        path = base_path / folder
        path.mkdir(parents=True,exist_ok=True)
        

def create_files(base_path:Path,files: list[str]):
    for file in files:
        path = base_path / file
        path.parent.mkdir(parents=True,exist_ok=True)
        
        path.touch()
        
def run_commands(base_path:Path,commands: list[str]):
    for command in commands:
        subprocess.run(command,shell=True, cwd=base_path)
        
def open_apps(base_path:Path,apps:list[str]):
    for app in apps:
        subprocess.Popen(
            app,
            shell=True,
            cwd=base_path
        )
        
def run_automations(base_path:Path,automation:dict):
    create_folders(base_path,automation["folders"])
    create_files(base_path,automation["files"])
    run_commands(base_path,automation["commands"])
    open_apps(base_path,automation["apps"])