import argparse
import configparser
import logging
import os
import sys
from functools import wraps
from pathlib import Path

from manim._config.utils import config_file_paths


def make_config_parser(custom_file: str = None):
    library_wide, user_wide, folder_wide = config_file_paths()
    parser = configparser.ConfigParser()
    with open(library_wide) as file:
        parser.read_file(file)  # necessary file
    
    with open(Path.resolve(Path(__file__).parent / "default.cfg")) as file:
        parser.read_file(file)

    other_files = [user_wide, custom_file if custom_file else folder_wide]
    parser.read(other_files)

    return parser


# def _parse_args(args: list) -> argparse.Namespace:
def parse_livestream_args(args: list):
    parser = argparse.ArgumentParser(
        description="Livestreaming configuration for Manim",
        prog="manim_livestream",
        usage="python -m %(prog)s [opts]",
    )
    parser.add_argument(
        "--use-ipython",
        help="Use IPython for streaming",
        action="store_const",
        const=True,
    )
    parser.add_argument(
        "--config_file",
        help="Specify the configuration file"
    )
    return parser.parse_args(args[1:])


def disable_logging(func):
    """Decorator for disabling logging output of a function."""

    wraps(func)

    def action(*args, **kwargs):
        logging.disable(50)
        func(*args, **kwargs)
        logging.disable(0)

    return action

