import code
import functools
import logging
import os
import readline
import rlcompleter
import subprocess
from functools import wraps

from manim._config import config, console, logger
from manim._config.main_utils import parse_args
from .streaming_scene import get_streamer, play_scene

from .utils import streaming_config
from .utils.utils import disable_logging

__all__ = ["livestream", "stream", "open_client"]


info = """
[green]Manim is now running in streaming mode. Stream animations by passing
them to manim.play(), e.g.[/green]

[cyan]>>> c = Circle()
>>> manim.play(ShowCreation(c))[/cyan]

[green]The current streaming class under the name `manim` inherits from the
original Scene class. To create a streaming class which inherits from
another scene class, e.g. MovingCameraScene, create it with the syntax:[/green]

[cyan]>>> manim2 = get_streamer(MovingCameraScene)[/cyan]

[green]Want to render the animation of an entire pre-baked scene? Here's an example:[/green]

[cyan]>>> from example_scenes import basic[/cyan]
[cyan]>>> play_scene(basic.WarpSquare)[/cyan]
[cyan]>>> play_scene(basic.OpeningManimExample, start=0, end=5)[/cyan]

[green]To view an image of the current state of the scene or mobject, use:[/green]

[cyan]>>> manim.show_frame()[/cyan]        [italic]# view image of current scene[/italic]
[cyan]>>> c = Circle()[/cyan]
[cyan]>>> c.show()[/cyan]                  [italic]# view image of Mobject[/italic]
"""


def open_client(client=None):
    """Opens the window for the streaming protocol player.

    Default player is ``ffplay``. Optional to be used on any other player
    that works similar to ``ffplay``.

    Note: Also useful to call when the player hangs to run it again.
    """
    command = [
        "ffplay",
        "-x",
        "1280",
        "-y",
        "360",  # For a resizeable window
        "-window_title",  # Name of the window
        "Livestream",
        "-loglevel",
        "quiet",
        "-protocol_whitelist",
        "file,rtp,udp",
        "-i",
        "streams\\stream_rtp.sdp",
        "-reorder_queue_size",
        "0",
    ]
    return subprocess.Popen(command)


@disable_logging
def guarantee_sdp_file():
    """Ensures, if required, that the sdp file exists,
    while supressing the loud info message given out by this process
    """
    sdp_path = os.path.join(config.media_dir, streaming_config.sdp_name)
    if not os.path.exists(sdp_path):
        kicker = get_streamer()
        kicker.wait()
        del kicker


@disable_logging
def popup_window():
    """Triggers the opening of the window. May lack utility for a streaming
    client like VLC.
    """
    get_streamer().wait(0.5)


def livestream():
    """Main function, enables livestream mode.

    This is called when running ``manim --livestream`` from the command line.

    Can also be called in a REPL, though the less activated version of this
    might be more suitable for quick sanity and testing checks.

    .. seealso::
        :func:`~.stream`
    """

    logger.debug("Ensuring sdp file exists: Running Wait() animation")
    guarantee_sdp_file()

    open_client()

    logger.debug("Triggering streaming client window: Running Wait() animation")
    popup_window()

    variables = {
        "manim": get_streamer(),
        "get_streamer": get_streamer,
        "play_scene": play_scene,
        "open_client": open_client,
    }

    if streaming_config.use_ipython:
        import manim
        from IPython import start_ipython

        console.print(info)
        variables.update(vars(manim).copy())
        start_ipython(argv=[], user_ns=variables)
        return

    readline.set_completer(rlcompleter.Completer(variables).complete)
    readline.parse_and_bind("tab: complete")
    shell = code.InteractiveConsole(variables)
    shell.push("from manim import *")
    shell.push("from .utils import streaming_config")

    console.print(info)
    shell.interact(banner="", exitmsg="")


def stream():
    """Convenience function for setting up streaming from a running REPL.

    Example
    -------

    >>> from manim import stream, Circle, ShowCreation
    >>> manim = stream()
    >>> circ = Circle()
    >>> manim.play(ShowCreation(circ))
    """
    guarantee_sdp_file()
    streamer = get_streamer()
    open_client()
    return streamer
