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

# ------------
# 3rd Party - From pip

import click
from rich.console import Console, RenderableType

console = Console()
error_console = Console(stderr=True)

# ------------
# Custom Modules

from .common import RichCommand

# from .common import file_hash, write_json, read_json

# from .create import create
# from .clip import clip

# -------------


@click.group(cls=RichCommand)
@click.version_option()
@click.pass_context
def main(ctx, *args, **kwargs):
    """
    Find all files recursively subject to `.gitignore` like excludes

    # Usage

    $ finder .

    """


    pass


# Add the child menu options
# main.add_command(create)
# main.add_command(clip)
