#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid       = 2ae7ea9e-85aa-11ec-aff7-25b28cecc0c5
# author     = Troy Williams
# email      = troy.williams@bluebill.net
# date       = 2022-02-04
# -----------

"""
"""

# ------------
# System Modules - Included with Python

from pathlib import Path

# ------------
# 3rd Party - From pip

import click
import toml

from rich.traceback import install
install(show_locals=True)

# ------------
# Custom Modules

# from .common import RichCommand

from .command_sync import sync
from .command_search import search

# -------------

@click.group()
@click.version_option()
@click.pass_context
@click.option(
    "--settings",
    multiple=True,
    type=click.Path(
        exists=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
    ),
    required=True,  # We need at least one settings. Make it required so we don't have to check for it ourselves
    help="TOML file to use. You can use multiple TOML files by specifying more --settings switches. ",
)
def main(*args, **kwargs):
    """
    Find all files recursively subject to `.gitignore` like excludes

    """

    ctx = args[0]
    ctx.ensure_object(dict)

    folders = []
    for cfg in kwargs['settings']:

        cfg = toml.loads(cfg.read_text())
        folders.extend(cfg['folders'])

    ctx.obj["folders"] = folders

    pass


# Add the child menu options
main.add_command(sync)
main.add_command(search)

