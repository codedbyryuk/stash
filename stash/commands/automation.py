import typer

app = typer.Typer()

@app.command()
def run(name:str,project:str):
    print(f"Running automation '{name}' for project '{project}'")