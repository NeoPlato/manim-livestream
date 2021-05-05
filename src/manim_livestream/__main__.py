import click
import cloup
from click_default_group import DefaultGroup
from manim import config
from manim.cli.render.ease_of_access_options import ease_of_access_options
from manim.cli.render.global_options import global_options
from manim.cli.render.output_options import output_options
from manim.cli.render.render_options import render_options

from . import __version__
from .cli import streaming_options
from .config import get_streaming_configurations
from .stream_starter import livestream


@cloup.command(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@streaming_options
@global_options
@output_options
@render_options
@ease_of_access_options
def main(**args):
    class ClickArgs:
        def __init__(self, args):
            parser = get_streaming_configurations()
            exec("self.use_ipython = {}".format(parser["CLI"]["use_ipython"]))
            for name in args:
                setattr(self, name, args[name])
            self.file = "-"
            self.scene_names = None

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

    click_args = ClickArgs(args)
    config.digest_args(click_args)

    livestream(click_args.use_ipython)
    return args


# @click.group(
#     cls=DefaultGroup,
#     default="start",
#     no_args_is_help=True,
#     help="Begin livestreaming",
#     # epilog=EPILOG,
# )
# @click.pass_context
# def main(ctx):
#     """The entry point for manim-livestream."""
#     pass

# main.add_command(start)

if __name__ == '__main__':
    main()
