import functools
from manim import config, logger


def disable_logging(func):
    """Decorator for disabling logging output of a function."""

    functools.wraps(func)
    def action(*args, **kwargs):
        logger.setLevel("ERROR")
        func(*args, **kwargs)
        logger.setLevel(config.verbosity)

    return action