import typer
from rich.console import Console
from pathlib import Path
from stash.commands.organize import organize
from stash.commands.rename import rename
from stash.commands.duplicates import duplicates

app = typer.Typer(
    help="Stash — remove the boring parts."
)

console = Console()

@app.callback()
def main():
    """Stash - a tiny CLI for eliminating repetitive tasks."""
    pass

@app.command()
def hello():
    """Test that Stash is working."""
    console.print("[bold green]⚡ Stash is alive.[/bold green]")

@app.command("organize")
def organize_command( path: Path = typer.Argument(..., help="Directory to organize.")):
    """Scan a directory and preview how files would be organized."""

    organize(path)

@app.command("rename")
def rename_target( path: Path = typer.Argument(..., help="File or folder to rename."),
                  new_name: str = typer.Argument(..., help="The new name for the file or folder.")):
    """Rename a file or a folder"""

    rename(path,new_name)

@app.command("duplicates")
def duplicate_command(path:Path = typer.Argument(...,help="Directory to scan for duplicate files.")):
    """Find duplicate files inside a directory"""

    duplicates(Path(path))