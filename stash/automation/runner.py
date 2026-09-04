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
        
def run_commands(commands: list[str]):
    for command in commands:
        subprocess.run(command,shell=True)