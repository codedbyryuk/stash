import typer
from rich.console import Console
from pathlib import Path
from stash.commands.organize import organize

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