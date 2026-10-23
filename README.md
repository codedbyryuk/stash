# About Stash

**Stash** is a Python CLI tool designed to eliminate boring and repetitive tasks. From organizing directories and finding duplicate files to automating project setups and managing your projects, Stash helps streamline your development workflow.

Stash is built with Python.

## Available Features

### `organize`

Organizes files in a directory into categories.

```bash
stash organize directory_name
```

### `rename`

Renames a file or folder.

```bash
stash rename file_name new_file_name
```

### `duplicates`

Finds duplicate files in a directory and lets you review and remove them.

```bash
stash duplicates directory_name
```

### `compress`

Compresses a file or folder into an archive.

```bash
stash compress directory_name
```

You can also specify a custom name for the compressed file:

```bash
stash compress directory_name -o new_name
```

### `find`

Finds files recursively by name or category.

Search by name:

```bash
stash find -n "file_name.txt"
```

Search by category, such as images, videos, or audio:

```bash
stash find -t image
```

### `automation`

Create, manage, and run reusable automation templates for project setup.

List available automations:

```bash
stash automation list
```

View an automation's details:

```bash
stash automation show python
```

Create a new automation:

```bash
stash automation create
```

Edit or delete an automation:

```bash
stash automation edit python
stash automation delete python
```

Run an automation to create a project:

```bash
stash automation run python my-project
```

Skip the confirmation prompt:

```bash
stash automation run python my-project --yes
```

Automations can create folders and files, execute commands, and open applications.

### Project Management

Stash can keep track of your projects, including projects created through its automation system.

**Register an existing project:**

```bash
stash register my-project "C:\path\to\project"
```

**List registered projects:**

```bash
stash projects
```

The project list displays registered paths and whether their directories are available.

**View project details:**

```bash
stash info my-project
```

Displays the project's path, availability, and the number of files and folders in its root directory.

**Open a project in VS Code:**

```bash
stash open my-project
```

**Open a project in File Explorer:**

```bash
stash open my-project --explorer
```

**Unregister a project:**

```bash
stash unregister my-project
```

Unregistering removes the project from Stash's registry without deleting its files.

## Tech

- Python
- Typer — CLI commands and arguments
- Rich — terminal output and tables
- pathlib — filesystem paths
- shutil — file operations
- hashlib — file hashing
- zipfile — archive creation
- subprocess — executing commands and opening applications
- JSON — storing automation templates and the project registry

## Note

**Stash is still in development.** Features and commands may change as development continues.