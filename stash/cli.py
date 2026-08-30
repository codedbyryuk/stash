import typer
from rich.console import Console


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