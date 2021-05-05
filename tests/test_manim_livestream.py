import os

from manim._config import config
import pytest 

from manim_livestream import __version__
from manim_livestream.stream_starter import guarantee_sdp_file
from manim_livestream.utils import streaming_config


def test_version():
    assert __version__ == "0.0.1"


@pytest.mark.parametrize(
    "directory, expected_path",
    [
        ("media_dir", "streams"),
        ("tex_dir", "streams/Tex"),
        ("text_dir", "streams/texts")
    ],
)
def test_custom_folders(directory, expected_path):
    assert config.get_dir(directory).as_posix() == expected_path


def test_sdp_file_created():
    file = os.path.join(config.media_dir, streaming_config.sdp_name)
    assert os.path.exists(file)