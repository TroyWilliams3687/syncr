#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid:   a6b8bb6c-85aa-11ec-aff7-25b28cecc0c5
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2022-02-04
# -----------

"""
"""

# ------------
# System Modules - Included with Python

from pathlib import Path

# ------------
# 3rd Party - From PyPI

import click

from rich.console import Console; console = Console()

# ------------
# Custom Modules

# -------------


def print_folder_details(folder):

    console.print(f'Source: [red]{folder["source"]}[/red]')

    if not Path(folder["source"]).expanduser().exists():
        console.print(f'[red]MISSING: {folder["source"]}[/red]')
        console.print()

    console.print(f'Destination:  [red]{folder["destination"]}[/red]')

    if not Path(folder["destination"]).expanduser().exists():
        console.print(f'[red]Does Not Exist! {folder["destination"]}[/red]')
        console.print()

    exclude_keys = (
        "exclude-dir-pattern",
        "exclude-file-pattern",
        "exclude-dir-path-pattern",
        "exclude-file-path-pattern",
    )

    console.print()

    for exclude_key in exclude_keys:

        if exclude_key in folder:
            console.print(
                f"[red]{exclude_key}[/red] -> [blue]{folder[exclude_key]}[/blue]"
            )


def find_files(folder: Path = None):
    """ """

    classified = {}

    if not folder.is_dir():
        raise ValueError(f"Not a directory! - {folder}")

    for p in folder.glob("*"):

        if p.is_dir():
            classified.setdefault("DIR", []).append(p)

        elif p.is_file():
            classified.setdefault("FILE", []).append(p)

        elif p.is_mount():
            classified.setdefault("MOUNT", []).append(p)

        elif p.is_symlink():
            classified.setdefault("SYMLINK", []).append(p)

        elif p.is_socket():
            classified.setdefault("SOCKET", []).append(p)

        elif p.is_fifo():
            classified.setdefault("FIFO", []).append(p)

        elif p.is_block_device():
            classified.setdefault("BLOCK_DEVICE", []).append(p)

        elif p.is_char_device():
            classified.setdefault("CHAR_DEVICE", []).append(p)

        else:
            classified.setdefault("UNKOWN", []).append(p)

    return classified
