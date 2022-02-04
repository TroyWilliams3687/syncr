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

# from .common import RichCommand

# from .common import file_hash, write_json, read_json

# from .create import create
# from .clip import clip

# -------------

def find_files(folder:Path = None):
    """
    """

    classified = {}

    if not folder.is_dir():
        raise ValueError(f'Not a directory! - {folder}')

    for p in folder.glob("*"):

        if p.is_dir():
            classified.setdefault('DIR', []).append(p)

        elif p.is_file():
            classified.setdefault('FILE', []).append(p)

        elif p.is_mount():
            classified.setdefault('MOUNT', []).append(p)

        elif p.is_symlink():
            classified.setdefault('SYMLINK', []).append(p)

        elif p.is_socket():
            classified.setdefault('SOCKET', []).append(p)

        elif p.is_fifo():
            classified.setdefault('FIFO', []).append(p)

        elif p.is_block_device():
            classified.setdefault('BLOCK_DEVICE', []).append(p)

        elif p.is_char_device():
            classified.setdefault('CHAR_DEVICE', []).append(p)

        else:
            classified.setdefault('UNKOWN', []).append(p)

    return classified


@click.command()
@click.argument("target", type=click.Path(exists=True))
@click.pass_context
def search(*args, **kwargs):
    """
    Search for files recursively.

    # Usage

    $ finder search ~/repositories/prototypes/pint

    """

    target = Path(kwargs["target"])

    console.print(f'Searching [red]{target}[/red]...')


    # see https://docs.python.org/3/library/fnmatch.html for details on
    # the wildcard files

    # if a directory is found here that matches raise and exception.
    # This is to make sure that we can avoid things like git repos or
    # other things that shouldn't be part of a onedrive sync.

    dir_excludes_fail = [
        '.git',
        '.hg',
    ]

    dir_excludes = [
        # '.*',
        '.git',
        '.venv',
        '.ipynb_checkpoints',
    ]

    file_excludes = [
        # '.gitignore',
        # 'Makefile.*'
        'Makefile.*.sample',
        'Makefile.env',
    ]

    for p, dirs, files in os.walk(target):

        for d in dirs:
            if any([fnmatch.fnmatch(d, pattern) for pattern in dir_excludes_fail]):
                raise ValueError(f'Found Exclude-Fail DIR - {Path(p).joinpath(d)}. Parent Path should be excluded.')

        # filter out the directories we don't want to search
        filtered_dir_list = []

        for d in dirs:

            if not any([fnmatch.fnmatch(d, pattern) for pattern in dir_excludes]):

                filtered_dir_list.append(d)

        dirs[:] = filtered_dir_list

        for f in files:

            # Filter the files
            if not any([fnmatch.fnmatch(f, pattern) for pattern in file_excludes]):

                # We made it this far, process the file.
                console.print(f'{Path(p).joinpath(f)}')
