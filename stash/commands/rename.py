from pathlib import Path
import typer
from rich.console import Console

console = Console()

def rename(target_path: Path,new_name:str):
    """Rename a file or a folder."""

    if not target_path.exists():
        console.print(f"\n[bold red]✗[/bold red] Path does not exist: {target_path}")
        raise typer.Exit(code=1)

    new_path = target_path.parent / new_name

    if new_path.exists():
        console.print(f"\n[bold red]✗[/bold red] Destination already exist: {new_path}")
        raise typer.Exit(code=1)

    try:
        target_path.rename(new_path)
        console.print(f"[bold green]✓[/bold green] Renamed '[bold]{target_path.name}[/bold]' to '[bold]{new_name}[/bold]'")
    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {e}")
        raise typer.Exit(code=1)