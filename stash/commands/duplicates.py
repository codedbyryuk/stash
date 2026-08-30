import hashlib
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

console = Console()


def get_file_hash(file: Path) -> str:
    hash_sha256 = hashlib.sha256()

    with file.open("rb") as f:
        while chunk := f.read(8192):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def get_files(path:Path)->list[Path]:
    return[file for file in path.iterdir() if file.is_file()]


def find_duplicates(files: list[Path])-> dict[str,list[Path]]:
    hashes ={}

    for file in files:
        file_hash = get_file_hash(file)

        if file_hash not in  hashes:
            hashes[file_hash] = []
        hashes[file_hash].append(file)

    return {
        file_hash: files
        for file_hash, files in hashes.items()
        if len(files) > 1
    }


def duplicates(path: Path):
    """Find duplicate files inside a directory"""

    if not path.exists():
        console.print(f"[bold red]✗[/bold red] Directory does not exist: {path}")
        raise typer.Exit(code=1)

    if not path.is_dir():
        console.print(f"[bold red]✗[/bold red] Not a directory: {path}")
        raise typer.Exit(code=1)

    files = get_files(path)

    if not files:
        console.print("[yellow]No files found.[/yellow]")
        return

    console.print(f"\n[bold cyan]Stash[/bold cyan] scanning "
                  f"[bold]{len(files)}[/bold] files...\n")

    duplicate_groups = find_duplicates(files)

    if not duplicate_groups:
        console.print("[bold green]✓[/bold green] No duplicates found.")
        return

    console.print(
        f"[bold yellow]Found {len(duplicate_groups)} "
        f"duplicate groups[/bold yellow]\n"
    )

    for number, (_,group) in enumerate(
        duplicate_groups.items(),
        start=1
    ):
        console.print(f"[bold]Group {number}[/bold]")

        for file in group:
            console.print(f"  {file}")

        console.print()