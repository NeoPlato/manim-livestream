from manim.renderer.cairo_renderer import CairoRenderer

from .stream_file_writer import StreamFileWriter


class StreamCairoRenderer(CairoRenderer):
    def init_scene(self, scene):
        """For compatibility with the __init__ from :class:`~.Scene` that's not 
        being directly overridden
        """
        self.file_writer = StreamFileWriter(self, "")
