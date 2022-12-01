#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid   = 40ff8d1a-860d-11ec-b000-23846d952ca6
# author = Troy Williams
# email  = troy.williams@bluebill.net
# date   = 2022-02-04
# -----------

"""
"""

# ------------
# System Modules - Included with Python

import os
import fnmatch

from pathlib import Path

# ------------
# 3rd Party - From pip

import click

from rich.console import Console

console = Console()

# ------------
# Custom Modules

from .common import print_folder_details

# -------------
# Typing

from typing import TypeVar

# https://docs.python.org/3/library/typing.html#typing.TypeVar
PathLike = TypeVar("PathLike", str, Path)

# -------------


def any_pattern_matches(item: str, patterns: list = None):
    """
    Given the item, does it match any of the patterns using `fnmatch`?
    """

    return any([fnmatch.fnmatch(item, pattern) for pattern in patterns])


def file_search(search_path: PathLike, verbose: int = 0, rules: dict = None):
    """
    Uses os.walk and iterates through the path recursively following the
    directory exclude patterns. It returns proper pathlib.Path objects
    representing valid files.

    # args

    search_path
        - A path liek object

    # kwargs

    verbose
        - Display status messages based on the verbosity level set.
        - Default = 0

    rules
        - A dictionary containing the fnmatch patterns to filter the
          files returns and the folders searched.
        - expected keys:
            - exclude-dir-pattern
                - A list of fnmatch patterns to match against
                - This can apply to any folder within the path

            - exclude-dir-path-pattern
                - A list of relative paths from the search path
                - the items is concatenated with the search path and the
                  directories are compared

            - exclude-file-pattern
                - A list of fnmatch patterns to match against the files
                - Apply to any file name within any folder

            - exclude-file-path-pattern
                - a list of relative file paths that are concatenated
                  with the current folder and compared against the
                  file

    # Return

    Every file that isn't filtered is returned, one at a time.

    """

    for current_path, dirs, files in os.walk(search_path):

        # current_path - the current path os.walk is on
        # dirs - the folders in the current path
        # files - the files in the current path

        cp = Path(current_path)

        if verbose >= 3:
            console.print(f"[blue]Current Folder: {cp}[/blue]")

        if "exclude-dir-pattern" in rules or "exclude-dir-path-pattern" in rules:

            filtered_dir_list = []

            for d in dirs:

                add_directory = True

                if "exclude-dir-pattern" in rules:

                    if any_pattern_matches(d, rules["exclude-dir-pattern"]):

                        if verbose >= 2:
                            console.print(f"[red]EXCLUDE-DIR[/red] -> [cyan]{d}[/cyan]")

                        add_directory = False

                if "exclude-dir-path-pattern" in rules:

                    if any_pattern_matches(
                        cp.joinpath(d), rules["exclude-dir-path-pattern"]
                    ):
                        if verbose >= 2:
                            console.print(
                                f"[red]EXCLUDE-DIR-FULL[/red] -> [cyan]{d}[/cyan]"
                            )

                        add_directory = False

                if add_directory:
                    filtered_dir_list.append(d)

            dirs[:] = filtered_dir_list

        for f in files:

            fp = cp.joinpath(f)

            if "exclude-file-pattern" in rules:

                if any_pattern_matches(f, rules["exclude-file-pattern"]):

                    if verbose >= 2:
                        console.print(f"[red]EXCLUDE-FILE[/red] -> [cyan]{f}[/cyan]")

                    continue

            if "exclude-file-path-pattern" in rules:

                if any_pattern_matches(
                    cp.joinpath(f), rules["exclude-file-path-pattern"]
                ):

                    if verbose >= 2:
                        console.print(
                            f"[red]EXCLUDE-FILE-FULL[/red] -> [cyan]{f}[/cyan]"
                        )

                    continue

            yield fp


@click.command()
@click.pass_context
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Display extra information about the process.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Display what would be copied, but doesn't actually copy.",
)
def sync(*args, **kwargs):
    """
    Sync the files in the source folder with the destination folder.

    # Usage

    $ syncr --settings=./sample/default.toml sync --dry-run --verbose --verbose --verbose

    $ syncr --settings=./sample/default.toml sync --dry-run -vvv

    """

    ctx = args[0]

    for folder in ctx.obj["folders"]:

        console.print()
        print_folder_details(folder)
        console.print()

        source_path = Path(folder["source"]).expanduser()
        destination_path = Path(folder["destination"]).expanduser()

        if "exclude-dir-path-pattern" in folder:

            folder["exclude-dir-path-pattern"] = [
                source_path.joinpath(d).resolve()
                for d in folder["exclude-dir-path-pattern"]
            ]

        if "exclude-file-path-pattern" in folder:
            folder["exclude-file-path-pattern"] = [
                source_path.joinpath(f).resolve()
                for f in folder["exclude-file-path-pattern"]
            ]

        for source_file_path in file_search(
            source_path, verbose=kwargs["verbose"], rules=folder
        ):

            destination_file_path = destination_path.joinpath(
                source_file_path.relative_to(source_path)
            )

            if destination_file_path.exists():

                # WE could probably do an SHA 256 HASH on the file to really compare things.

                # is the source file newer than the destination file?
                if (
                    source_file_path.stat().st_mtime
                    > destination_file_path.stat().st_mtime
                ):

                    console.print(
                        f"[green]EXISTS - OLDER[/green] -> {source_file_path.relative_to(source_path)}"
                    )

                else:

                    if kwargs["verbose"] >= 1:
                        console.print(
                            f"[red]EXISTS[/red] -> {source_file_path.relative_to(source_path)}"
                        )

                    continue

            if source_file_path.is_file():

                if not kwargs["dry_run"]:

                    try:

                        destination_file_path.parent.mkdir(parents=True, exist_ok=True)

                    except FileNotFoundError as fe:
                        console.print(f'[red]{fe}[/red]')

                    console.print(
                        f"COPYING: {source_file_path.relative_to(source_path)}"
                    )

                    try:
                        destination_file_path.write_bytes(source_file_path.read_bytes())

                    except FileNotFoundError as fe:
                        console.print(f'[red]{fe}[/red]')


                else:

                    console.print(
                        f"COPYING ([cyan]DRY RUN[/cyan]): {source_file_path.relative_to(source_path)}"
                    )
