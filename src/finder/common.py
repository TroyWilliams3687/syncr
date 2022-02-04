#!/usr/bin/env python3
#-*- coding:utf-8 -*-

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

from typing import TYPE_CHECKING, List, NoReturn, Optional, Tuple

# ------------
# 3rd Party - From PyPI

import click

from rich.console import Console #, RenderableType
# from rich.markup import escape
from rich.text import Text

# ------------
# Custom Modules

# -------------


# https://github.com/cookiejar/cookietemple/blob/master/cookietemple/custom_cli/click.py

def blend_text(
    message: str, color1: Tuple[int, int, int], color2: Tuple[int, int, int]
) -> Text:
    """Blend text from one color to another."""
    text = Text(message)
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    dr = r2 - r1
    dg = g2 - g1
    db = b2 - b1
    size = len(text)
    for index in range(size):
        blend = index / size
        color = f"#{int(r1 + dr * blend):2X}{int(g1 + dg * blend):2X}{int(b1 + db * blend):2X}"
        text.stylize(color, index, index + 1)
    return text

# https://github.com/Textualize/rich-cli/blob/644937a392e32ce7a462ae79c9ab539b6ffb4b0b/src/rich_cli/__main__.py#L144-L218
# Eventually, this might be in a pip project, for now, just use this one

class RichCommand(click.Command):
    """Override Clicks help with a Richer version."""

    # TODO: Extract this in to a general tool, i.e. rich-click

    def format_help(self, ctx, formatter):

        from rich.highlighter import RegexHighlighter
        from rich.panel import Panel
        from rich.table import Table
        from rich.theme import Theme

        class OptionHighlighter(RegexHighlighter):
            highlights = [
                r"(?P<switch>\-\w)",
                r"(?P<option>\-\-[\w\-]+)",
            ]

        highlighter = OptionHighlighter()

        console = Console(
            theme=Theme(
                {
                    "option": "bold cyan",
                    "switch": "bold green",
                }
            ),
            highlighter=highlighter,
        )

        # console.print(
        #     f"[b]Rich CLI[/b] [magenta]v[/] 🤑\n\n[dim]Rich text and formatting in the terminal\n",
        #     justify="center",
        # )

        # console.print(
        #     "Usage: [b]rich[/b] [b][OPTIONS][/] [b cyan]<PATH,TEXT,URL, or '-'>\n"
        # )

        options_table = Table(highlight=True, box=None, show_header=False)

        for param in self.get_params(ctx)[1:]:

            if len(param.opts) == 2:
                opt1 = highlighter(param.opts[1])
                opt2 = highlighter(param.opts[0])

            else:
                opt2 = highlighter(param.opts[0])
                opt1 = Text("")

            if param.metavar:
                opt2 += Text(f" {param.metavar}", style="bold yellow")

            options = Text(" ".join(reversed(param.opts)))
            help_record = param.get_help_record(ctx)

            if help_record is None:
                help = ""

            else:
                help = Text.from_markup(param.get_help_record(ctx)[-1], emoji=False)

            if param.metavar:
                options += f" {param.metavar}"

            options_table.add_row(opt1, opt2, highlighter(help))

        console.print(
            Panel(
                options_table, border_style="dim", title="Options", title_align="left"
            )
        )

        console.print(
            blend_text("♥ https://www.textualize.io", (32, 32, 255), (255, 32, 255)),
            justify="right",
        )
