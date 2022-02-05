# Syncr

A utility to copy files from one folder to another and maintain the relative folder structure. The idea is to copy files to a sync folder maintained by Onedrive or Dropbox while that folder is maintained by something else. 

## Installation

### Git Repo

Clone the git repo:

```bash
$ git clone git@github.com:TroyWilliams3687/syncr.git
```

### Create the Virtual Environment

You can use the `Makefile` to create the virtual environment and install all requirements automatically:

```bash
$ make venv
```

Otherwise you will have to create the virtual environment manually and install the dependencies traditionally after activating the environment.

## Activating the Virtual Environment

### Linux

On Linux, for most causes you can simple using the `Makefile` to build the system. If you need to activate the virtual environment:

```bash
$ make shell
```

Or manually:


```bash
$ . .venv/bin/activate
```

### Windows

Activate the virtual environment that you want to install it too.

On Windows, using powershell:

```bash
$ .\.venv\Scripts\activate.ps1
```

## Usage


```bash
$ syncr --settings=./sample/default.toml sync --dry-run --verbose --verbose --verbose
```

```bash
$ syncr --settings=./sample/default.toml sync --dry-run -vvv
```

```bash
$ syncr --settings=./sample/default.toml search excludes
```

```bash
$ syncr --settings=./sample/default.toml search excludes --files --dir
```

## Configuration

You can use as many different configuration files as you like. They are [TOML](https://toml.io/en/) formatted and easy to use. The look like:


```toml
[[folders]]

# The source path we want to copy files recursively from
source = '~/repositories/projects/documentos'

# The destination where we want to copy the files to, matching the folder
# structure
destination = '~/tmp/find_files_testing'

# exclude-dir-pattern - Directory patterns we want to exclude from the
# destination folder. It will match any directory in any of the sub-directory
# levels. If a directory name matches one of the patterns it is excluded.
# NOTE: This is optional and doesn't need to be included.
exclude-dir-pattern = [
    ".git",
    ".venv",
    ".pytest_cache",
    "__pycache__",
    "*.egg-info",
    ".ipynb_checkpoints",

]

# exclude-dir-path-pattern - These patterns will be joined with the source path.
# It will filter out specific folders within the source tree. The pattern
# should be relative to the source path.
# NOTE: This is optional and doesn't need to be included.
# NOTE: This doesn't support wildcards. It is supposed to be an exact match filter
exclude-dir-path-pattern = [
    "samples/configuration",
    "en/documents",
]

# exclude-file-pattern - File matching patterns we want to exclude from the
# destination folder. Any file name that matches a pattern will be excluded.
# The patterns are applied to every file that is discovered.
# NOTE: This is optional and doesn't need to be included.
exclude-file-pattern = [
    ".gitignore",
#    "Makefile.*",
    "Makefile.*.sample",
#    "Makefile.env",
]


# exclude-file-path-pattern - These patterns will be joined with the source
# path. It will filter out specific files within the tree. The pattern should
# be relative to the source path.
# NOTE: This is optional and doesn't need to be included.
exclude-file-path-pattern = [
    "src/documentos/plugins/toc_plugins.py",
]
```

The main part is the `[[folders]]` section. These define the different source and destinations folders as well as the various excludes applied to each section. The following is a bare minimum configuration file:

```toml
[[folders]]

# The source path we want to copy files recursively from
source = '~/repositories/projects/documentos'

# The destination where we want to copy the files to, matching the folder
# structure
destination = '~/tmp/find_files_testing'
```

With the folders section of the TOML file, you can define the `exclude-dir-pattern` list. These are directory names that will be ignored when copying files from the source to the destination folders. They follow the [fnmatch](https://docs.python.org/3/library/fnmatch.html) wildcards.

| Pattern | Meaning                          |
|---------|----------------------------------|
| *       | matches everything               |
| ?       | matches any single character     |
| [seq]   | matches any character in seq     |
| [!seq]  | matches any character not in seq |


```toml
# exclude-dir-pattern - Directory patterns we want to exclude from the
# destination folder. It will match any directory in any of the sub-directory
# levels. If a directory name matches one of the patterns it is excluded.
# NOTE: This is optional and doesn't need to be included.
exclude-dir-pattern = [
    ".git",
    ".venv",
    ".pytest_cache",
    "__pycache__",
    "*.egg-info",
    ".ipynb_checkpoints",

]
```

You can also define the `exclude-dir-path-pattern` and define fixed paths within the source folder that you want to ignore/exclude. This is the relative path that when combined with the source path gives the full path to exclude.


```toml
# exclude-dir-path-pattern - These patterns will be joined with the source path.
# It will filter out specific folders within the source tree. The pattern
# should be relative to the source path.
# NOTE: This is optional and doesn't need to be included.
# NOTE: This doesn't support wildcards. It is supposed to be an exact match filter
exclude-dir-path-pattern = [
    "samples/configuration",
    "en/documents",
]
```

The file names can be defined with the `exclude-file-pattern` list. These are names that will be ignored when copying files from the source to the destination folders. They follow the [fnmatch](https://docs.python.org/3/library/fnmatch.html) wildcards.

```toml
# exclude-file-pattern - File matching patterns we want to exclude from the
# destination folder. Any file name that matches a pattern will be excluded.
# The patterns are applied to every file that is discovered.
# NOTE: This is optional and doesn't need to be included.
exclude-file-pattern = [
    ".gitignore",
#    "Makefile.*",
    "Makefile.*.sample",
#    "Makefile.env",
]

```

You can also define the `exclude-file-path-pattern` and define fixed paths to the files within the source folder that you want to ignore/exclude. This is the relative path that when combined with the source path gives the full path to exclude.

```toml
# exclude-file-path-pattern - These patterns will be joined with the source
# path. It will filter out specific files within the tree. The pattern should
# be relative to the source path.
# NOTE: This is optional and doesn't need to be included.
exclude-file-path-pattern = [
    "src/documentos/plugins/toc_plugins.py",
]
```

>NOTE: These variables do not have to exist in your TOML file or have to be defined for each section.

## License

[MIT](https://choosealicense.com/licenses/mit/)

