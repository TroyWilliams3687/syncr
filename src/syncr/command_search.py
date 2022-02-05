#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid   = 4e87b8a4-8680-11ec-bf72-8386de55c3c1
# author = Troy Williams
# email  = troy.williams@bluebill.net
# date   = 2022-02-05
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


def pattern_tester(value, pattern_key, patterns, source_path=None):
    """
    A simple method to output if the value string matches a pattern.
    """

    if pattern_key in patterns:
        for pattern in patterns[pattern_key]:
            if fnmatch.fnmatch(value, pattern):
                console.print(f'[red]{pattern_key.upper()}[/red]: [cyan]{source_path}[/cyan] -> matches [blue]`{pattern}`[/blue]')


@click.group()
@click.pass_context
def search(*args, **kwargs):
    """
    Search the source folder and display the excludes.

    # Usage

    $ syncr --settings=./config/default.toml search excludes

    $ syncr --settings=./config/default.toml search excludes --files --dir

    """

    pass


@search.command()
@click.pass_context
@click.option(
    "--dir", is_flag=True, help="Display directories that match `exclude-dir-pattern`."
)
@click.option(
    "--dir-path", is_flag=True, help="Display files that match `exclude-dir-path-pattern`."
)
@click.option(
    "--file", is_flag=True, help="Display files that match `exclude-file-pattern`."
)
@click.option(
    "--file-path", is_flag=True, help="Display files that match `exclude-file-path-pattern`."
)
def excludes(*args, **kwargs):
    """
    Display the files that match the exclude filters. This is the
    reverse of the sync process. This method is designed to help make
    sure the filters are working correctly.

    There are optional switches. If not switches are specified, then it
    assumes that you want to see all of the options.

    # Usage

    $ syncr --settings=./config/default.toml search excludes

    $ syncr --settings=./config/default.toml search excludes --files --dir

    """

    ctx = args[0]

    switch_keys = ['file', 'file_path', 'dir']
    if not any(kwargs[key] for key in switch_keys):

        for switch_key in switch_keys:
            kwargs[switch_key] = True

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

            if kwargs['dir_path'] and 'exclude-dir-path-pattern' in folder:
                for pattern in folder['exclude-dir-path-pattern']:

                    if cp == pattern:
                        console.print(f'[red]EXCLUDE-DIR-PATH-PATTERN[/red]: [cyan]{cp}[/cyan]')

            for d in dirs:

                if kwargs['dir']:
                    pattern_tester(d, 'exclude-dir-pattern', folder, source_path=cp.joinpath(d).relative_to(source_path))

            for f in files:

                source_file_path = cp.joinpath(f)

                if kwargs['file_path'] and 'exclude-file-path-pattern' in folder:
                    for pattern in folder['exclude-file-path-pattern']:

                        if source_file_path == pattern:
                            console.print(f'[red]EXCLUDE-FILE-PATH-PATTERN[/red]: [cyan]{cp}[/cyan]')

                if kwargs['file']:
                    pattern_tester(f, 'exclude-file-pattern', folder, source_path=source_file_path.relative_to(source_path))

    console.print()



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
