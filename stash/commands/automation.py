from pathlib import Path

from stash.automation.manager import load_automation
from stash.automation.runner import create_folders,create_files,run_commands

automation = load_automation(Path("automations/python.json"))

project = Path("test-projects")

create_folders(
    project,
    automation["folders"]
)
create_files(
    project,
    automation["files"]
)

run_commands(automation["commands"])