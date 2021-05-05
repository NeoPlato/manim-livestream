import click
from cloup import option, option_group

streaming_options = option_group(
    "Streaming options",
    option(
        "--use-ipython",
        is_flag=True,
        help="Use IPython in the interactive console",
    ),
    option(
        "-sp",
        "--streaming_protocol",
        type=click.Choice(
            ["rtp", "udp"],
            case_sensitive=False,
        ),
        help="Streaming protocol to use for livestreaming configuration",
    ),
)
