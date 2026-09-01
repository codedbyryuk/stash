from pathlib import Path
from rich.console import Console
import typer

console = Console()

FILE_TYPES = {
    "image": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "video": {".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "audio": {".mp3", ".wav", ".flac", ".ogg", ".m4a"},
    "document": {".pdf", ".doc", ".docx", ".txt", ".md"},
    "archive": {".zip", ".tar", ".gz", ".7z", ".rar"},
    "code": {
        ".py",
        ".html",
        ".cpp",
        ".c",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".css",
        ".lua",
    },
}


def find_files(
    path: Path, name: str | None = None, file_type: str | None = None
) -> list[Path]:
    if path.is_file():
        files = [path]
    else:
        files = [file for file in path.rglob("*") if file.is_file()]

    if name:
        files = [file for file in files if file.match(name)]

    if file_type:
        file_type = file_type.lower()
        if file_type not in FILE_TYPES:
            console.print(
                f"[bold red]✗[/bold red] Unknown file type: {file_type}"
                f"\n Available types: image, video, audio, code, document, archive"
            )
            raise typer.Exit(code=1)
        extensions = FILE_TYPES[file_type]

        
        files = [file for file in files if file.suffix.lower() in extensions]

    return files


def find(path: Path, name: str | None = None, file_type: str | None = None):
    """Find files inside a directory."""

    if not path.exists():
        console.print(f"[bold red]✗[/bold red] " f"Path does not exist: {path}")
        raise typer.Exit(code=1)

    files = find_files(path, name, file_type)

    console.print(
        f"\n[bold cyan]Stash[/bold cyan] found " f"[bold]{len(files)}[/bold] files:\n"
    )

    for file in files:
        console.print(f"  {file}")
