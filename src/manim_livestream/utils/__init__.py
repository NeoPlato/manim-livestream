__all__ = ["streaming_config"]

import sys
from pathlib import Path

from manim._config import config
from manim._config.main_utils import parse_args

from .utils import make_config_parser, parse_livestream_args


def get_configuration():

    class StreamingConfig:
        def __init__(self, **kwargs):
            vars(self).update(kwargs)

        def _get_kwargs(self):
            return list(self.__dict__.items())

        def __eq__(self, other):
            if not isinstance(other, StreamingConfig):
                return NotImplemented
            return vars(self) == vars(other)

        def __contains__(self, key):
            return key in self.__dict__

        def __repr__(self):
            return str(self.__dict__)

    livestream_args = list(arg for arg in sys.argv if arg in ('--use-ipython', '--config_file'))
    other_args = list(arg for arg in sys.argv if arg not in livestream_args)
    other_args.insert(1, "")
    other_args.append("--config_file")
    other_args.append("{}".format(Path.resolve(Path(__file__).parent / "default.cfg")))
    other_args.append("--custom_folders")
    livestream_args = parse_livestream_args(livestream_args)
    config = StreamingConfig()
    config.use_ipython = livestream_args.use_ipython

    parser = make_config_parser(custom_file=livestream_args.config_file)
    streaming_config = dict(parser['streaming'].items())
    for key, value in streaming_config.items():
        setattr(config, key, value.format(**streaming_config))

    # If streaming config has been acquired, ensure config utilizes
    # the special settings as well, since sys.argv is a hacky way of 
    # communicating with manim

    return config, other_args


streaming_config, argv = get_configuration()
args = parse_args(argv)
config.digest_args(args)


