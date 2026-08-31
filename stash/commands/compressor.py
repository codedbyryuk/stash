from zipfile import ZipFile,ZIP_DEFLATED
from pathlib import Path
from rich.console import Console
import typer


console = Console()

def get_files(path:Path)->list[Path]:
    if path.is_file():
        return [path]
    
    return [
        file 
        for file in path.rglob("*")
        if file.is_file()
    ]
    

def compress(path:Path,output:Path):
    files = get_files(path)
    
    
    if not files:
        console.print(
            "[yellow]No files to compress.[/yellow]"
        )
        return
    
    with ZipFile(
        output,
        'w',
        compression=ZIP_DEFLATED
    ) as zip_file:
        for file in files:
            zip_file.write(
                file,
                arcname=file.relative_to(path.parent)
            )
            
    console.print(
        f"[bold green]✓[/bold green] "
        f"Created {output}"
    )