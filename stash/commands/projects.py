import typer
from rich.console import Console
from pathlib import Path
from stash.projects import (register_project,load_projects,unregister_project)
from rich.table import Table
import subprocess


app = typer.Typer()
console = Console()

@app.command("register", help="Register an existing project with Stash.")
def register(
    name:str,
    path:Path
):
    try:
        register_project(name,path)
    except ValueError as err:
        console.print(f"[bold red]✗[/bold red] {err}")
        raise typer.Exit(code=1)
    
    console.print(
        f"[bold green]✓[/bold green] "
        f"Registered project '[cyan]{name}[/cyan]'."
    )

@app.command("projects", help="List registered projects.")
def list_project():
    from stash.projects import load_projects
    
    data = load_projects()
    
    projects = data["projects"]
    
    if not projects:
        console.print("[yellow]No projects registered yet.[/yellow]")
        raise typer.Exit()
    
    table = Table(title="Your Projects")
    
    table.add_column("Name",style="cyan")
    table.add_column("Path",style="white")
    table.add_column("Status",style="green")
    
    for name, details in projects.items():
        path = Path(details["path"])
        status  ="Available" if path.is_dir else "Missing"
        
        table.add_row(name,str(path),status)
        
    console.print(table)
    

@app.command("info", help="Show details about a registered project.")
def project_info(name: str):
    data = load_projects()
    projects = data["projects"]

    if name not in projects:
        console.print(
            f"[bold red]✗[/bold red] "
            f"Project '{name}' is not registered."
        )
        raise typer.Exit(code=1)

    details = projects[name]
    path = Path(details["path"])

    console.print(f"\n[bold cyan]{name}[/bold cyan]")
    console.print(f"Path: {path}")
    console.print(
        f"Status: {'Available' if path.is_dir() else 'Missing'}"
    )

    if path.is_dir():
        items = list(path.iterdir())
        files = sum(item.is_file() for item in items)
        folders = sum(item.is_dir() for item in items)

        console.print(f"Files in root: {files}")
        console.print(f"Folders in root: {folders}")


@app.command("open", help="Open a registered project in VS Code or File Explorer.")
def open_project(
    name: str,
    explorer: bool = typer.Option(
        False,
        "--explorer",
        help="Open the project in File Explorer."
    ),
):
    data = load_projects()
    projects = data["projects"]

    if name not in projects:
        console.print(
            f"[bold red]✗[/bold red] "
            f"Project '{name}' is not registered."
        )
        raise typer.Exit(code=1)

    path = Path(projects[name]["path"])

    if not path.is_dir():
        console.print(
            f"[bold red]✗[/bold red] "
            f"Project directory does not exist: {path}"
        )
        raise typer.Exit(code=1)

    try:
        if explorer:
            subprocess.Popen(["explorer", str(path)])
        else:
            vscode = (
                Path.home()
                / "AppData"
                / "Local"
                / "Programs"
                / "Microsoft VS Code"
                / "Code.exe"
            
            )
            if vscode.is_file():
                subprocess.Popen([str(vscode), str(path)])
            else:
                console.print(
                     "[bold red]✗[/bold red] VS Code was not found."
                )
                raise typer.Exit(code=1)
    except FileNotFoundError:
        console.print(
            "[bold red]✗[/bold red] "
            "Could not find the requested application. "
            "Check that it is installed and available on PATH."
        )
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]✓[/bold green] Opening '[cyan]{name}[/cyan]'."
    )


@app.command("unregister", help="Remove a project from the registry without deleting its files.")
def unregister(name: str):
    data = load_projects()

    if name not in data["projects"]:
        console.print(
            f"[bold red]✗[/bold red] "
            f"Project '{name}' is not registered."
        )
        raise typer.Exit(code=1)

    confirmed = typer.confirm(
        f"Unregister project '{name}'? "
        "Its files will NOT be deleted."
    )

    if not confirmed:
        console.print("[yellow]Cancelled.[/yellow]")
        raise typer.Exit()

    unregister_project(name)

    console.print(
        f"[bold green]✓[/bold green] "
        f"Unregistered project '[cyan]{name}[/cyan]'."
    )
