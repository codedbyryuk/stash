import json
import typer
from pathlib import Path
from rich.console import Console
from stash.projects import register_project
from stash.automation.manager import load_automation
from stash.automation.runner import run_automations

app = typer.Typer()
console = Console()


def load_automation_safely(path: Path) -> dict:
    try:
        return load_automation(path)
    except ValueError as error:
        console.print(f"[bold red]✗ Invalid automation:[/bold red] {error}")
        raise typer.Exit(code=1)


AUTOMATIONS_DIR = (
    Path(__file__).resolve().parents[2] / "automations"
)


@app.command()
def run(
    name: str,
    project: str,
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation.",
    ),
):
    automation_file = AUTOMATIONS_DIR / f"{name}.json"

    if not automation_file.exists():
        console.print(
            f"[bold red]✗[/bold red] "
            f"Automation '{name}' not found."
        )
        raise typer.Exit(code=1)

    automation = load_automation_safely(automation_file)
    project_path = Path(project).resolve()

    console.print("\n[bold cyan]Stash — Automation Preview[/bold cyan]")
    console.print(f"Automation: [bold]{name}[/bold]")
    console.print(f"Project:    [bold]{project_path}[/bold]")

    console.print("\n[bold]Folders:[/bold]")
    for folder in automation.get("folders", []):
        console.print(f"  + {folder}")

    console.print("\n[bold]Files:[/bold]")
    for file in automation.get("files", []):
        console.print(f"  + {file}")

    console.print("\n[bold]Commands:[/bold]")
    for command in automation.get("commands", []):
        console.print(f"  $ {command}")

    console.print("\n[bold]Apps:[/bold]")
    for app_name in automation.get("apps", []):
        console.print(f"  > {app_name}")

    if not yes:
        confirmed = typer.confirm(
            "\nRun this automation?"
        )

        if not confirmed:
            console.print("[yellow]Cancelled.[/yellow]")
            raise typer.Exit()

    project_path.mkdir(parents=True, exist_ok=True)
    try:
        run_automations(project_path, automation)
    except RuntimeError as error:
        console.print(
            f"\n[bold red]✗[/bold red] {error}"
        )
        raise typer.Exit(code=1)
    
    try:
        register_project(project_path.name, project_path)
    except ValueError as error:
        console.print(f"[yellow]Warning:[/yellow] {error}")

    console.print(
        f"\n[bold green]✓[/bold green] "
        f"Project created at {project_path}"
    )
    
    
@app.command("list")
def list_automations():
    automation_files = sorted(
        AUTOMATIONS_DIR.glob("*.json")
    )
    if not automation_files:
        console.print("[yellow]No automations found.[/yellow]")
        return
    console.print("\n[bold cyan]Stash — Available Automations[/bold cyan]\n")
    
    for file in automation_files:
        automation = load_automation(file)
        
        name =  automation.get("name",file.stem)
        description = automation.get(
            "description",
            "No description provided."
        )
        
        console.print(
            f"[bold green]{name}[/bold green]:"
            f" {description}\n"
        )


@app.command("create")
def create_automation():
    name = typer.prompt("Automation name")
    description = typer.prompt("Description")

    automation_file = AUTOMATIONS_DIR / f"{name}.json"

    if automation_file.exists():
        console.print(
            f"[bold red]✗[/bold red] "
            f"Automation '{name}' already exists."
        )
        raise typer.Exit(code=1)

    folders = []
    files = []

    console.print(
        "\n[bold cyan]Folders[/bold cyan]"
    )
    console.print("Enter folder names one at a time.")
    console.print("Leave blank when finished.")

    while True:
        folder = typer.prompt("Folder", default="")
        if not folder:
            break
        folders.append(folder)

    console.print(
        "\n[bold cyan]Files[/bold cyan]"
    )
    console.print("Enter file paths one at a time.")
    console.print("Leave blank when finished.")

    while True:
        file = typer.prompt("File", default="")
        if not file:
            break
        files.append(file)
        
    
    commands = []

    console.print(
        "\n[bold cyan]Commands[/bold cyan]"
    )
    console.print("Enter commands to run during setup.")
    console.print("Leave blank when finished.")

    while True:
        command = typer.prompt("Command", default="")
        if not command:
            break
        commands.append(command)

    apps = []

    console.print(
        "\n[bold cyan]Apps[/bold cyan]"
    )
    console.print("Enter apps to open after setup.")
    console.print("Examples: code ., godot")
    console.print("Leave blank when finished.")

    while True:
        app_name = typer.prompt("App", default="")
        if not app_name:
            break
        apps.append(app_name)


    automation = {
        "name": name,
        "description": description,
        "folders": folders,
        "files": files,
        "commands": commands,
        "apps": apps
    }

    with automation_file.open("w", encoding="utf-8") as file:
        json.dump(automation, file, indent=4)

    console.print(
        f"\n[bold green]✓[/bold green] "
        f"Created automation '{name}'!"
    )


@app.command("show")
def show_automation(name: str):
    automation_file = AUTOMATIONS_DIR / f"{name}.json"

    if not automation_file.exists():
        console.print(
            f"[bold red]✗[/bold red] "
            f"Automation '{name}' not found."
        )
        raise typer.Exit(code=1)

    automation = load_automation_safely(automation_file)

    console.print(
        f"\n[bold cyan]{automation.get('name', name)}[/bold cyan]"
    )
    console.print(
        automation.get("description", "No description")
    )

    sections = [
        ("Folders", "folders"),
        ("Files", "files"),
        ("Commands", "commands"),
        ("Apps", "apps"),
    ]

    for title, key in sections:
        console.print(f"\n[bold]{title}:[/bold]")

        items = automation.get(key, [])

        if not items:
            console.print("  [dim]None[/dim]")
            continue

        for item in items:
            console.print(f"  • {item}")


@app.command("delete")
def delete_automation(name: str):
    automation_file = AUTOMATIONS_DIR / f"{name}.json"

    if not automation_file.exists():
        console.print(
            f"[bold red]✗[/bold red] "
            f"Automation '{name}' not found."
        )
        raise typer.Exit(code=1)

    confirmed = typer.confirm(
        f"Are you sure you want to delete '{name}'?"
    )

    if not confirmed:
        console.print("[yellow]Cancelled.[/yellow]")
        raise typer.Exit()

    automation_file.unlink()

    console.print(
        f"[bold green]✓[/bold green] "
        f"Deleted automation '{name}'."
    )



@app.command("edit")
def edit_automation(name: str):
    automation_file = AUTOMATIONS_DIR / f"{name}.json"

    if not automation_file.exists():
        console.print(
            f"[bold red]✗[/bold red] "
            f"Automation '{name}' not found."
        )
        raise typer.Exit(code=1)

    automation = load_automation_safely(automation_file)

    console.print(
        f"\nEditing automation: [bold cyan]{name}[/bold cyan]"
    )

    description = typer.prompt(
        "Description",
        default=automation.get("description", "")
    )
    automation["description"] = description

    console.print("\n[bold]Current folders:[/bold]")
    for folder in automation["folders"]:
        console.print(f"  - {folder}")

    if typer.confirm("\nDo you want to replace the folders?"):
        folders = []

        while True:
            folder = typer.prompt(
                "Folder path (leave empty to finish)",
                default=""
            )

            if not folder:
                break

            folders.append(folder)

        automation["folders"] = folders
    
    console.print("\n[bold]Current files:[/bold]")
    for file in automation["files"]:
        console.print(f"  - {file}")

    if typer.confirm("\nDo you want to replace the files?"):
        files = []

        while True:
            file = typer.prompt(
                "File path (leave empty to finish)",
                default=""
            )

            if not file:
                break

            files.append(file)

        automation["files"] = files
        
    
    console.print("\n[bold]Current commands:[/bold]")
    for command in automation["commands"]:
        console.print(f"  - {command}")

    if typer.confirm("\nDo you want to replace the commands?"):
        commands = []

        while True:
            command = typer.prompt(
                "Command (leave empty to finish)",
                default=""
            )

            if not command:
                break

            commands.append(command)

        automation["commands"] = commands

    
    console.print("\n[bold]Current apps:[/bold]")
    for app in automation["apps"]:
        console.print(f"  - {app}")

    if typer.confirm("\nDo you want to replace the apps?"):
        apps = []

        while True:
            app = typer.prompt(
                "App command (leave empty to finish)",
                default=""
            )

            if not app:
                break

            apps.append(app)

        automation["apps"] = apps


    with automation_file.open("w", encoding="utf-8") as file:
        json.dump(automation, file, indent=4)

    console.print(
        f"\n[bold green]✓[/bold green] "
        f"Updated automation '{name}'."
    )
