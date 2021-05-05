import code
import os
from pathlib import Path
import readline
import rlcompleter

from manim._config import config, console, logger
from .streaming_scene import get_streamer

from .config import streaming_config
from .config.logger_utils import disable_logging
from .utils import open_client, popup_window, guarantee_sdp_file

__all__ = ["livestream", "stream", "open_client"]


INFO = """
[green]Manim is now running in streaming mode. Stream animations by passing
them to self.play(), e.g.[/green]

[cyan]>>> c = Circle()
>>> self.play(ShowCreation(c))[/cyan]

[green]The current streaming class under the name `manim` inherits from the
original Scene class. To create a streaming class which inherits from
another scene class, e.g. MovingCameraScene, create it with the syntax:[/green]

[cyan]>>> self2 = get_streamer(MovingCameraScene)[/cyan]

[green]To view an image of the current state of the scene or mobject, use:[/green]

[cyan]>>> self.show_frame()[/cyan]        [italic]# view image of current scene[/italic]
[cyan]>>> c = Circle()[/cyan]
[cyan]>>> c.show()[/cyan]                  [italic]# view image of Mobject[/italic]
"""


def livestream(use_ipython):
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

    variables = dict(
        self=get_streamer(),
        get_streamer=get_streamer,
        play_scene=play_scene,
        open_client=open_client,
        streaming_config=streaming_config
    )

    if use_ipython:
        import manim
        from IPython import start_ipython

        console.print(INFO)
        variables.update(vars(manim))
        start_ipython(argv=[], user_ns=variables)
        return

    readline.set_completer(rlcompleter.Completer(variables).complete)
    readline.parse_and_bind("tab: complete")
    shell = code.InteractiveConsole(variables)
    shell.push("from manim import *")

    console.print(INFO)
    shell.interact(banner="", exitmsg="")


def play_scene(scene):
    """Play a scene using the livestreaming configuration

    Parameters
    ----------
    scene
        The scene to be played.
    """
    logger.debug("Ensuring sdp file exists: Running Wait() animation")
    guarantee_sdp_file()

    open_client()

    logger.debug("Triggering streaming client window: Running Wait() animation")
    popup_window(delay=2)

    scene.render()


def stream():
    """Convenience function for setting up streaming from a running REPL.

    Example
    -------
    
    >>> from manim_livestream import stream
    >>> from manim import Circle, ShowCreation
    >>> self = stream()
    >>> circ = Circle()
    >>> self.play(ShowCreation(circ))
    """
    guarantee_sdp_file()
    streamer = get_streamer()
    open_client()
    return streamer
