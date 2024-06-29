# syncr

## Introduction

A utility to copy files from one folder to another and maintain the relative folder structure. The idea is to copy files to a sync folder maintained by Onedrive or Dropbox while that folder is maintained by something else.

## QuickStart

1. [Install Rye](#installation-and-configuration)
2. [Installation and Configuration](#rye-sync)
3. [Activate](#activate-virtual-environment---traditional-approach)


## Installation and Configuration

To get this project up and running from the repository, it uses [Rye](https://rye-up.com) as the build/dependency manager. There are [instructions](https://rye-up.com/guide/installation/) for installing Rye on many different systems. This set of instructions are for Linux and windows. See the installation guide for other operating systems.

You have to download Rye to your system. Follow the [installation guide](https://rye-up.com/guide/installation/) for your operating system.

Why Rye? That is a good question. Python is a great language but it is tough to create a reproducible environment. You have to have the correct version of Python installed or available. You have to have the correct tools configured. If you are on Linux/BSD you have to make sure that your work doesn't mess up your system Python installation. It is fairly trivial if you are experienced, but annoying enough to have to do it over-and-over again. If you are new, it can be extremely difficult.

Rye takes care of handling the different versions of Python and managing the tools you need for a reproducible environment, particularly if you are doing cross-platform work.

### Linux

For Linux, you can use the following:

```bash
curl -sSf https://rye-up.com/get | bash
```

There are also good guides to configuring Rye for your shell. Here is what I had to do to get it working in ZSH on my system.

Edit **.zshrc**:

```bash
vi ~/.zshrc
```

Add the following:

```bash
source "$HOME/.rye/env"
```

Restart the terminal and type **rye**. To add [shell completion](https://rye-up.com/guide/installation/#shell-completion), you can:

```bash
mkdir $ZSH_CUSTOM/plugins/rye
rye self completion -s zsh > $ZSH_CUSTOM/plugins/rye/_rye
```

### Windows

For windows, download the [installer](https://github.com/mitsuhiko/rye/releases/latest/download/rye-x86_64-windows.exe) listed in the installation guide link.

## Basic Rye Usage

### Rye Update

[Update rye](https://rye-up.com/guide/installation/#updating-rye):

```bash
rye self update
```

### Rye Sync

Once you have rye properly installed, you can run [**rye sync**](https://rye-up.com/guide/commands/sync/), to build (or update) the virtual environment.

Create/Update Virtual Environment

```bash
rye sync
```

> NOTE: This needs to be run from within the repository. If you add new dependencies or modify the **pyproject.toml** you should run **rye sync**.

### Activate Virtual Environment - Traditional Approach

You can add the following alias to your **.zshrc** or **.bashrc**, or you can run the activate script directly:

```bash
# Python Virtual Environment Alias
alias activate="source .venv/bin/activate"
```

>NOTE: On Windows, there is an **activate.ps1**, a PowerShell script that you can execute.

## Usage

```bash
syncr --settings=./sample/default.toml sync --dry-run --verbose --verbose --verbose
```

```bash
syncr --settings=./sample/default.toml sync --dry-run -vvv
```

```bash
syncr --settings=./sample/default.toml search excludes
```

```bash
syncr --settings=./sample/default.toml search excludes --files --dir
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

Please refer to [LICENSE.md](LICENSE.md).

