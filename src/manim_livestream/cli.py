import click
from cloup import option, option_group

streaming_options = option_group(
    "Streaming options",
    option(
        "--use-ipython",
        is_flag=True,
        help="Use IPython as the interactive console",
    ),
    option(
        "--protocol",
        help="Use a custom streaming protocol",
        default=None
    ),
    option(
        "--client",
        help="Specify the streaming client to use",
        default=None
    )
)
