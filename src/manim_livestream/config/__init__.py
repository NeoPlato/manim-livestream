from pathlib import Path
import configparser

__all__ = ["streaming_config"]


def get_streaming_configurations():
    parser = configparser.ConfigParser()
    config_path = Path.resolve(Path(__file__).parent / "default.cfg")
    
    with open(config_path) as file:
        parser.read_file(file)

    return parser


class StreamingConfig:
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value.format(**kwargs))

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
    

streaming_config = StreamingConfig(**get_streaming_configurations()["streaming"])


