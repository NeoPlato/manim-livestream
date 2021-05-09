import os
import subprocess
from pathlib import Path

from manim import __version__
from manim._config import config, logger
from manim.constants import FFMPEG_BIN
from manim.scene.scene_file_writer import SceneFileWriter

from .config import streaming_config


class StreamFileWriter(SceneFileWriter):
    """Specialized file writer for streaming.

    Takes a good portion of its implementation from `:class:~.SceneFileWriter`
    but changes enough of it to redirect output directories and the final
    request to the streaming protocol.

    .. seealso::

        :func:`~.stream_starter.livestream`
        :class:`~.SceneFileWriter`

    """

    def init_output_directories(self, scene_name):
        """Overridden to avoid creation of unnecessary output directories."""
        pass

    def open_movie_pipe(self, file_path=None):
        """Overridden to stream the output directly to the streaming protocol
        """
        logger.info(
            "Houston, we are ready to launch. Sending over to %(url)s",
            {"url": {streaming_config.url}},
        )

        fps = config["frame_rate"]
        if config["use_opengl_renderer"]:
            width, height = self.renderer.get_pixel_shape()
        else:
            height = config["pixel_height"]
            width = config["pixel_width"]

        sdp_path = os.path.join(
            Path(__file__).parent, 
            streaming_config.sdp_name
        )

        command = [
            FFMPEG_BIN,
            "-y",  # overwrite output file if it exists
            "-f",
            "rawvideo",
            "-s",
            "%dx%d" % (width, height),  # size of one frame
            "-pix_fmt",
            "rgba",
            "-r",
            str(fps),  # frames per second
            "-i",
            "-",  # The input comes from a pipe
            "-an",  # Tells FFMPEG not to expect any audio
            "-loglevel",
            config["ffmpeg_loglevel"].lower(),
            "-metadata",
            f"comment=Rendered with Manim Community v{__version__}",
        ]
        if config["use_opengl_renderer"]:
            command += ["-vf", "vflip"]
        if config["transparent"]:
            command += ["-vcodec", "qtrle"]
        else:
            command += ["-vcodec", "libx264", "-pix_fmt", "yuv420p"]
        if streaming_config.protocol == "rtp":
            command += ["-sdp_file", sdp_path]
        command += [
            "-f",
            "rtp",
            streaming_config.url,
        ]
        self.writing_process = subprocess.Popen(command, stdin=subprocess.PIPE)

    def close_movie_pipe(self):
        self.writing_process.stdin.close()
        self.writing_process.wait()
