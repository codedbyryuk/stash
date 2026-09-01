# About Stash

**Stash** is a CLI tool which allows user to eliminate boring and repetitive tasks. From organizing directories to automating project setups, **Stash** can be used.

**Stash** is made with purely using python.

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

Finds a specific file by name.

```bash
stash find -n "file_name.txt"
```

You can also search for files by category, such as images, videos, or audio:

```bash
stash find -t image
```

## Tech

- typer
- rich
- shutil
- pathlib
- hashlib
- zipfile

## Note

**Stash** is still in development so there are only few commands.