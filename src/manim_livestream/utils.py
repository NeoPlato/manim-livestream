import os
import subprocess
from pathlib import Path

from manim import config

from .config import streaming_config
from .config.logger_utils import disable_logging
from .streaming_scene import get_streamer


def open_client(client=None):
    """Opens the window for the streaming protocol player.

    Default player is ``ffplay``. Optional to be used on any other player
    that works similar to ``ffplay``.

    Note: Also useful to call when the player hangs to run it again.
    """
    sdp_path = os.path.join(
        Path(__file__).parent, 
        streaming_config.sdp_name
    )
    command = [
        streaming_config.streaming_client,
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
        sdp_path,
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
def popup_window(delay=0.5):
    """Triggers the opening of the window. May lack utility for a streaming
    client like VLC.
    """
    get_streamer().wait(delay)
