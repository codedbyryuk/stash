import typer
from rich.console import Console
from pathlib import Path
from stash.commands.organize import organize
from stash.commands.rename import rename
from stash.commands.duplicates import duplicates
from stash.commands.compressor import compress
from stash.commands.find import find

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
    
@app.command("compress")
def compress_command(
    path:Path=typer.Argument(...,help="Directory or file to compress."),
    output: str= typer.Option(
        None,
        "--output",
        "-o",
        help="output zip filename."
    )):
    """Compress a file or a directory into a ZIP archive."""
    
    source = Path(path)
    
    if not source.exists():
        console.print(
            f"[bold red]✗[/bold red] "
            f"Path does not exist: {source}"
        )
        raise typer.Exit(code=1)
    
    if output:
        output_path = Path(output)
    else:
        output_path = Path(f"{source.name}.zip")
    
    compress(source,output_path)
    
@app.command("find")
def find_command(
    path:Path=typer.Argument(...,help="Directory or file to search"),
    name: str | None = typer.Option(
        None,
        "--name",
        "-n",
        help="Filter files by name pattern."
    ),
    file_type: str | None = typer.Option(
        None,
        "--type",
        "-t",
        help="Filter by file type."
    )):
    """Find files recursively."""
    
    find(Path(path),name,file_type)