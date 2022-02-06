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


# https://gist.github.com/Esperanzq/3ee8a03e845c98bc12546272802cb41b
# def get_all_files(path, min_size_kb=None):
#     for root, dirs, files in os.walk(path):
#         for file_ in files:
#             path = os.path.abspath(os.path.join(root, file_))
#             size = (os.path.getsize(path)) // 1024
#             if size >= min_size_kb:
#                 yield ("{} - {} kb".format(path, size))


# files_lazy_lister = get_all_files("F:\\", min_size_kb=1000)
# pprint.pprint(list(files_lazy_lister))

def file_search(search_path, verbose=0, rules=None):
    """
    Uses os.walk and iterates through the path recursively following the
    directory exclude patterns. It returns proper pathlib.Path objects
    representing valid files.
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
                    if any(
                        [
                            fnmatch.fnmatch(d, pattern)
                            for pattern in rules["exclude-dir-pattern"]
                        ]
                    ):

                        # This test failed, skip the rest of the tests
                        if verbose >= 2:
                            console.print(f"[red]EXCLUDE-DIR -> {d}[/red]")

                        add_directory = False

                if "exclude-dir-path-pattern" in rules:

                    if any(
                        cp.joinpath(d) == pattern
                        for pattern in rules["exclude-dir-path-pattern"]
                    ):

                        if verbose >= 2:
                            console.print(f"[red]EXCLUDE-DIR -> {d}[/red]")

                        add_directory = False

                if add_directory:
                    filtered_dir_list.append(d)

            dirs[:] = filtered_dir_list

        for f in files:

            fp = cp.joinpath(f)

            if "exclude-file-pattern" in rules:
                if any(
                    [
                        fnmatch.fnmatch(f, pattern)
                        for pattern in rules["exclude-file-pattern"]
                    ]
                ):
                    continue

            if "exclude-file-path-pattern" in rules:

                if any(
                    fp == pattern
                    for pattern in rules["exclude-file-path-pattern"]
                ):
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

        for source_file_path in file_search(source_path, verbose=kwargs['verbose'], rules=folder):

            destination_file_path = destination_path.joinpath(
                source_file_path.relative_to(source_path)
            )


            if destination_file_path.exists():

                # WE could probably do an SHA 256 HASH on the file to really compare things.

                # is the source file newer than the destination file?
                if source_file_path.stat().st_mtime > destination_file_path.stat().st_mtime:

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

                    destination_file_path.parent.mkdir(parents=True, exist_ok=True)

                    console.print(
                        f"COPYING: {source_file_path.relative_to(source_path)}"
                    )
                    destination_file_path.write_bytes(source_file_path.read_bytes())

                else:

                    console.print(
                        f"COPYING ([cyan]DRY RUN[/cyan]): {source_file_path.relative_to(source_path)}"
                    )


        # -----------
        # for current_path, dirs, files in os.walk(source_path):

        #     # current_path - the current path os.walk is on
        #     # dirs - the folders in the current path
        #     # files - the files in the current path

        #     cp = Path(current_path)

        #     if kwargs["verbose"] >= 3:
        #         console.print(f"[blue]Current Folder: {cp}[/blue]")

        #     # ------------

        #     if "exclude-dir-pattern" in folder or "exclude-dir-path-pattern" in folder:

        #         filtered_dir_list = []

        #         for d in dirs:

        #             add_directory = True

        #             if "exclude-dir-pattern" in folder:
        #                 if any(
        #                     [
        #                         fnmatch.fnmatch(d, pattern)
        #                         for pattern in folder["exclude-dir-pattern"]
        #                     ]
        #                 ):

        #                     # This test failed, skip the rest of the tests
        #                     if kwargs["verbose"] >= 2:
        #                         console.print(f"[red]EXCLUDE-DIR -> {d}[/red]")

        #                     add_directory = False

        #             if "exclude-dir-path-pattern" in folder:

        #                 if any(
        #                     cp.joinpath(d) == pattern
        #                     for pattern in folder["exclude-dir-path-pattern"]
        #                 ):
        #                     # filtered_dir_list.append(d)

        #                     if kwargs["verbose"] >= 2:
        #                         console.print(f"[red]EXCLUDE-DIR -> {d}[/red]")

        #                     add_directory = False

        #             if add_directory:
        #                 filtered_dir_list.append(d)

        #         dirs[:] = filtered_dir_list

        #     for f in files:

        #         source_file_path = cp.joinpath(f)

        #         if "exclude-file-pattern" in folder:
        #             if any(
        #                 [
        #                     fnmatch.fnmatch(f, pattern)
        #                     for pattern in folder["exclude-file-pattern"]
        #                 ]
        #             ):
        #                 continue

        #         if "exclude-file-path-pattern" in folder:

        #             if any(
        #                 source_file_path == pattern
        #                 for pattern in folder["exclude-file-path-pattern"]
        #             ):
        #                 continue

        #         destination_file_path = destination_path.joinpath(
        #             cp.relative_to(source_path)
        #         ).joinpath(f)

        #         if destination_file_path.exists():

        #             # WE could probably do an SHA 256 HASH on the file to really compare things.

        #             # is the source file newer than the destination file?
        #             if source_file_path.stat().st_mtime > destination_file_path.stat().st_mtime:

        #                 console.print(
        #                     f"[green]EXISTS - OLDER[/green] -> {source_file_path.relative_to(source_path)}"
        #                 )

        #             else:

        #                 if kwargs["verbose"] >= 1:
        #                     console.print(
        #                         f"[red]EXISTS[/red] -> {source_file_path.relative_to(source_path)}"
        #                     )

        #                 continue

        #         if source_file_path.is_file():

        #             if not kwargs["dry_run"]:

        #                 destination_file_path.parent.mkdir(parents=True, exist_ok=True)

        #                 console.print(
        #                     f"COPYING: {cp.relative_to(source_path).joinpath(f)}"
        #                 )
        #                 destination_file_path.write_bytes(source_file_path.read_bytes())

        #             else:

        #                 console.print(
        #                     f"COPYING ([cyan]DRY RUN[/cyan]): {cp.relative_to(source_path).joinpath(f)}"
        #                 )
