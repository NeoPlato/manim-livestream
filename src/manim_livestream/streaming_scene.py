from manim import config
from manim.mobject.frame import FullScreenRectangle as Frame
from manim.scene.scene import Scene, EndSceneEarlyException, RerunSceneException
from manim.utils.simple_functions import get_parameters

from .stream_renderer import StreamCairoRenderer

__all__ = ["get_streamer"]


class Stream:
    """Abstract base class.

    This class is really intended for inheritance of the style::
        >>> class Streamer(Stream, Scene): # doctest: +SKIP
        ...     pass
        ...
        >>>

    This order is paramount. This :class:`Stream` class carries out the switch to
    the specialized renderer, which uses :class:`StreamFileWriter` to
    handle specialized streaming services. That explains the calls to ``super``,
    which digs through the MRO of a class instead of using just a single
    implementation contained in Scene.

    .. note::

        This class is not intended to be used on its own and will
        most likely raise errors if done so.
    """

    def __init__(self, **kwargs):
        camera_class = self.mint_camera_class()
        renderer = StreamCairoRenderer(camera_class=camera_class)
        super().__init__(renderer=renderer, **kwargs)
        # To identify the frame in a black background
        self.add(Frame())
        self.setup()

    @classmethod
    def mint_camera_class(cls):
        """A camera class from the scene's inheritance hierarchy.

        Only ``__init__`` methods in :class:`~.Scene` classes and derived classes
        from this have the camera class required for the renderer. This declaration
        for the entire class exists only here, and for that reason it is the only place
        to look.

        Raises
        ------
        AttributeError
            If this lookup fails.
        """

        for obj in cls.mro():
            try:
                parameter = get_parameters(obj.__init__)["camera_class"]
            except KeyError:
                continue
            else:
                return parameter.default
        raise AttributeError("Object does not contain scene protocol")

    def show_frame(self):
        """Opens the current frame in the Default Image Viewer
        of your system.
        """
        self.renderer.update_frame(self, ignore_skipping=True)
        self.renderer.camera.get_image().show()

    def render(self, preview=False):
        """
        Renders this Scene.

        Parameters
        ---------
        preview : bool
            If true, opens scene in a file viewer.
        """
        self.setup()
        try:
            self.construct()
        except EndSceneEarlyException:
            pass
        except RerunSceneException as e:
            self.remove(*self.mobjects)
            self.renderer.clear_screen()
            self.renderer.num_plays = 0
            return True
        self.tear_down()


def get_streamer(*scene):
    """
    Parameters
    ----------
    scene
        The scene whose methods can be used in the resulting
        instance, such as zooming in and arbitrary method constructions.
        Defaults to just Scene

    Returns
    -------
    StreamingScene
        A scene suited for streaming.
    """
    bases = (Stream,) + (scene or (Scene,))
    cls = type("StreamingScene", bases, {})
    # This class doesn't really need a name, but a generic one is permissible
    return cls()
