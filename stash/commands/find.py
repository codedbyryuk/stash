from pathlib import Path
from rich.console import Console
import typer


console = Console()


def find_files(path:Path,name:str | None=None)->list[Path]:
    if path.is_file():
        files = [path]
    else:
        files =[
            file
            for file in path.rglob("*")
            if file.is_file()
        ]
    
    if name:
        files=[
            file
            for file in files
            if file.match(name)
            
        ]
        
    return files
    


def find(path:Path,name: str | None=None):
    """Find files inside a directory."""
    
    if not path.exists():
        console.print(
            f"[bold red]✗[/bold red] "
            f"Path does not exist: {path}"
        )
        raise typer.Exit(code=1)
    
    files = find_files(path,name)
    
    console.print(
        f"\n[bold cyan]Stash[/bold cyan] found "
        f"[bold]{len(files)}[/bold] files:\n"
    )
    
    for file in files:
        console.print(f"  {file}")