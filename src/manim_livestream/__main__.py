from pathlib import Path

import click
import cloup
from click_default_group import DefaultGroup
from manim import config, console
from manim.cli.render.ease_of_access_options import ease_of_access_options
from manim.cli.render.global_options import global_options
from manim.cli.render.output_options import output_options
from manim.cli.render.render_options import render_options
from manim.utils.module_ops import scene_classes_from_file

from .cli import streaming_options
from .config import get_streaming_configurations, streaming_config
from .stream_starter import livestream, play_scene
from .streaming_scene import get_streamer


@cloup.command(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.argument("file", type=Path, required=False, default="-")
@click.argument("scene_names", required=False, nargs=-1)
@streaming_options
@global_options
@output_options
@render_options
@ease_of_access_options
def main(**args):
    class ClickArgs:
        def __init__(self):
            parser = get_streaming_configurations()
            exec("self.use_ipython = {}".format(parser["CLI"]["use_ipython"]))
            for name in args:
                if name in streaming_config and args[name] is not None:
                    setattr(streaming_config, name, args[name])
                setattr(self, name, args[name])

        def _get_kwargs(self):
            return list(self.__dict__.items())

        def __eq__(self, other):
            if not isinstance(other, ClickArgs):
                return NotImplemented
            return vars(self) == vars(other)

        def __contains__(self, key):
            return key in self.__dict__

        def __repr__(self):
            return str(self.__dict__)

    click_args = ClickArgs()
    config.digest_args(click_args)

    file = args["file"]
    if str(file) == "-":
        livestream(click_args.use_ipython)
    else:
        for SceneClass in scene_classes_from_file(file):
            try:
                scene = get_streamer(SceneClass)
                play_scene(scene)
            except Exception:
                console.print_exception()

if __name__ == '__main__':
    main()
