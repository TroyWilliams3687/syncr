#!/usr/bin/env python3
#-*- coding:utf-8 -*-

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

# from .common import RichCommand

# from .common import file_hash, write_json, read_json

# from .create import create
# from .clip import clip

# -------------



@click.command()
@click.pass_context
@click.option(
    "--verbose", is_flag=True, help="Display extra information about the process."
)
def sync(*args, **kwargs):
    """
    Sync the files in the source folder with the destination folder.

    # Usage

    $ syncr --settings=./config/default.toml sync


    """

    ctx = args[0]

    # for folder in ctx.obj["folders"]:

    #     console.print()
    #     print_folder_details(folder)
    #     console.print()

    #     source_path = Path(folder['source']).expanduser()
    #     destination_path = Path(folder['destination']).expanduser()

    #     for current_path, dirs, files in os.walk(source_path):

    #         cp = Path(current_path)

    #         # get the dir excludes working

    #         for f in files:

    #             source_file_path = cp.joinpath(f)
    #             destination_file_path = destination_path.joinpath(cp.relative_to(source_path)).joinpath(f)

    #             if destination_file_path.exists():
    #                 # could add date checks and copy if newer
    #                 continue

    #             destination_file_path.parent.mkdir(parents=True, exist_ok=True)

    #             if source_file_path.is_file():
    #                 console.print(f'COPYING: {cp.relative_to(source_path)/f}')
    #                 destination_file_path.write_bytes(source_file_path.read_bytes())



    for folder in ctx.obj["folders"]:

        console.print()
        print_folder_details(folder)
        console.print()

        source_path = Path(folder['source']).expanduser()
        destination_path = Path(folder['destination']).expanduser()

        if 'exclude-dir-path-pattern' in folder:

            folder['exclude-dir-path-pattern'] = [
                source_path.joinpath(d).resolve()
                for d in folder['exclude-dir-path-pattern']
            ]

        if 'exclude-file-path-pattern' in folder:
            folder['exclude-file-path-pattern'] = [
                source_path.joinpath(f).resolve()
                for f in folder['exclude-file-path-pattern']
            ]

        for current_path, dirs, files in os.walk(source_path):

            # current_path - the current path os.walk is on
            # dirs - the folders in the current path
            # files - the files in the current path

            cp = Path(current_path)

            # ------------
            filtered_dir_list = []

            for d in dirs:

                if 'exclude-dir-pattern' in folder:
                    if not any([fnmatch.fnmatch(d, pattern) for pattern in folder['exclude-dir-pattern']]):
                        filtered_dir_list.append(d)

                    else:
                        # This test failed, skip the rest of the tests
                        continue

                if 'exclude-dir-path-pattern' in folder:

                    if not any(cp.joinpath(d) == pattern for pattern in folder['exclude-dir-path-pattern']):
                        filtered_dir_list.append(d)

            dirs[:] = filtered_dir_list
            # ------------


            for f in files:

                source_file_path = cp.joinpath(f)

                if 'exclude-file-pattern' in folder:
                    if any([fnmatch.fnmatch(f, pattern) for pattern in folder['exclude-file-pattern']]):
                        continue

                if 'exclude-file-path-pattern' in folder:

                    if any(source_file_path == pattern for pattern in folder['exclude-file-path-pattern']):
                        continue

                destination_file_path = destination_path.joinpath(cp.relative_to(source_path)).joinpath(f)

                if destination_file_path.exists():
                    # could add date checks and copy if newer
                    console.print(f'[red]EXISTS[/red] -> {source_file_path.relative_to(source_path)}')
                    continue

                destination_file_path.parent.mkdir(parents=True, exist_ok=True)

                if source_file_path.is_file():
                    console.print(f'COPYING: {cp.relative_to(source_path)/f}')
                    destination_file_path.write_bytes(source_file_path.read_bytes())




    # --------------------
    # target = Path(kwargs["target"])

    # console.print(f'Searching [red]{target}[/red]...')


    # # see https://docs.python.org/3/library/fnmatch.html for details on
    # # the wildcard files

    # # if a directory is found here that matches raise and exception.
    # # This is to make sure that we can avoid things like git repos or
    # # other things that shouldn't be part of a onedrive sync.

    # dir_excludes_fail = [
    #     '.git',
    #     '.hg',
    # ]

    # dir_excludes = [
    #     # '.*',
    #     '.git',
    #     '.venv',
    #     '.ipynb_checkpoints',
    # ]

    # file_excludes = [
    #     # '.gitignore',
    #     # 'Makefile.*'
    #     'Makefile.*.sample',
    #     'Makefile.env',
    # ]

    # for p, dirs, files in os.walk(target):

    #     for d in dirs:
    #         if any([fnmatch.fnmatch(d, pattern) for pattern in dir_excludes_fail]):
    #             raise ValueError(f'Found Exclude-Fail DIR - {Path(p).joinpath(d)}. Parent Path should be excluded.')

    #     # filter out the directories we don't want to search
    #     filtered_dir_list = []

    #     for d in dirs:

    #         if not any([fnmatch.fnmatch(d, pattern) for pattern in dir_excludes]):

    #             filtered_dir_list.append(d)

    #     dirs[:] = filtered_dir_list

    #     for f in files:

    #         # Filter the files
    #         if not any([fnmatch.fnmatch(f, pattern) for pattern in file_excludes]):

    #             # We made it this far, process the file.
    #             console.print(f'{Path(p).joinpath(f)}')
