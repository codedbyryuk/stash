from pathlib import Path
import typer
import shutil
from rich.console import Console
from rich.table import Table

console = Console()

FILE_CATEGORIES = {
    "Images" : [".png",".jpeg",".jpg",".gif",".webp",".svg"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".ogg", ".m4a"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".ts", ".jsx", ".tsx", ".cpp", ".c", ".java"],
    "Executables": [".exe", ".msi", ".deb", ".AppImage"],
}

def get_category(file:Path) -> str:
    extension = file.suffix.lower()

    for category,extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Other"


def organize(path: Path):
    """Organize files inside a directory."""

    if not path.exists():
        console.print(
            f"[bold red]✗[/bold red] Directory does not exist: {path}"
        )
        raise typer.Exit(code=1)

    if not path.is_dir():
        console.print(
            f"[bold red]✗[/bold red] Not a directory: {path}"
        )
        raise typer.Exit(code=1)

    files = [file for file in path.iterdir() if file.is_file()]

    if not files:
        console.print("[yellow]No files found.[/yellow]")
        return

    categories = {}

    for file in files:
        category = get_category(file)

        if category not in categories:
            categories[category] = []

        categories[category].append(file)

    console.print(
        f"\n[bold cyan]⚡ Stash[/bold cyan] scanned "
        f"[bold]{len(files)}[/bold] files.\n"
    )

    table = Table(title="Organization Preview")

    table.add_column("Category")
    table.add_column("Files", justify="right")

    for category, category_files in sorted(categories.items()):
        table.add_row(category, str(len(category_files)))

    console.print(table)

    console.print(
        "\n[bold yellow]Nothing has been moved yet.[/bold yellow]"
    )

    verify_organization = input("Want to organize the folder? (y/n): ")

    if verify_organization=="y":

        console.print("\n [bold green]Moving files...[/bold green]")

        for category,category_files in categories.items():
            target_dir = path / category
            target_dir.mkdir(exist_ok=True)

            for file in category_files:
                destination = target_dir / file.name

                if destination.exists():
                    console.print(f"[dim]Skipping {file.name} (already exists in {category})[/dim]")
                    continue

                shutil.move(str(file),str(destination))


        console.print("[bold green]✓ Organization complete![/bold green]")
    else:
        return