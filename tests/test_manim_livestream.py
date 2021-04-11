import os

from manim_livestream import __version__
from manim_livestream.stream_starter import guarantee_sdp_file
from manim_livestream.utils import streaming_config
from manim._config import config


def test_version():
    assert __version__ == "0.0.1"


def test_sdp_file_created():
    file = os.path.join(config.media_dir, streaming_config.sdp_name)
    assert os.path.exists(file)


# I can't think of any other unit tests right now



