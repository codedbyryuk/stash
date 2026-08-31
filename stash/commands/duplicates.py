import hashlib
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()


def get_file_hash(file: Path) -> str:
    hash_sha256 = hashlib.sha256()

    with file.open("rb") as f:
        while chunk := f.read(8192):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def get_files(path: Path) -> list[Path]:
    return [file for file in path.iterdir() if file.is_file()]


def find_duplicates(files: list[Path]) -> dict[str, list[Path]]:

    files_by_size = {}

    for file in files:
        size = file.stat().st_size
        if size not in files_by_size:
            files_by_size[size] = []

        files_by_size[size].append(file)

    hashes = {}

    for size, same_size_files in files_by_size.items():
        if len(same_size_files) < 2:
            continue

        for file in track(same_size_files,description="Hashing files..."):
            file_hash = get_file_hash(file)

            if file_hash not in hashes:
                hashes[file_hash] = []

            hashes[file_hash].append(file)

    duplicates = {}

    for file_hash, same_hash_file in hashes.items():
        if len(same_hash_file) > 1:
            duplicates[file_hash] = same_hash_file

    return duplicates

def delete_file(file:Path)->bool:
    try:
        file.unlink()
        return True
    
    except OSError as error:
        console.print(
            f"[bold red]✗[/bold red] "
            f"Could not delete {file}: {error}"
        )
        return False

def choose_file_to_keep(files: list[Path]) -> Path | None:
    console.print("[bold]Choose a file to keep:[/bold]")

    for number, file in enumerate(files, start=1):
        console.print(f"  [{number}] {file}")

    console.print("  Skip this group (s)")

    while True:
        choice = typer.prompt("Your choice")

        if choice.lower() == "s":
            return None

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(files):
                return files[number - 1]

        console.print(
            "[red]Invalid choice. Try again.[/red]"
        )
        
def process_duplicate_group(files: list[Path]):
    keep = choose_file_to_keep(files)

    if keep is None:
        console.print(
            "[yellow]Skipped this group.[/yellow]\n"
        )
        return

    console.print(
        f"\n[bold green]✓ Keeping:[/bold green] {keep}"
    )

    for file in files:
        if file == keep:
            continue

        if delete_file(file):
            console.print(
                f"[bold red]Deleted:[/bold red] {file}"
            )

    console.print()

def calculate_reclaimable_space(duplicate_groups: dict[str, list[Path]]) -> int:
    total = 0

    for files in duplicate_groups.values():
        file_size = files[0].stat().st_size
        duplicate_counts = len(files) - 1

        total += file_size * duplicate_counts

    return total


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

    console.print(
        f"\n[bold cyan]Stash[/bold cyan] scanning "
        f"[bold]{len(files)}[/bold] files...\n"
    )

    duplicate_groups = find_duplicates(files)

    reclaimable = calculate_reclaimable_space(duplicate_groups)

    if not duplicate_groups:
        console.print("[bold green]✓[/bold green] No duplicates found.")
        return

    console.print(
        f"[bold yellow]Found {len(duplicate_groups)} "
        f"duplicate groups[/bold yellow]\n"
    )
    console.print(
        f"[bold cyan]Potentially reclaimable: "
        f"{reclaimable / (1024 ** 2):.2f} MB[/bold cyan]\n"
    )

    for number, (_, group) in enumerate(duplicate_groups.items(), start=1):
        console.print(f"[bold]Group {number}[/bold]")

        

        console.print(f"\n[bold]Group {number}[/bold]")
        process_duplicate_group(group)
