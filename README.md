# Manim Livestream

This plugin is designed to enable livestreaming support for [Manim](https://www.manim.community/). 
## Installation

Works like other packages, so pip will do fine

``` {.sourceCode .bash}
pip install manim-livestream
```


## Usage

- Run the following command:

```bash
python -m manim_livestream
```

This loads a python shell along with the usage information:

```bash
Manim is now running in streaming mode. Stream animations by passing
them to self.play(), e.g.

>>> c = Circle()
>>> self.play(ShowCreation(c))

The current streaming class under the name `manim` inherits from the
original Scene class. To create a streaming class which inherits from
another scene class, e.g. MovingCameraScene, create it with the syntax:

>>> self2 = get_streamer(MovingCameraScene)

To view an image of the current state of the scene or mobject, use:

>>> self.show_frame()        # view image of current scene
>>> c = Circle()
>>> c.show()                 # view image of Mobject

>>> 
```

- Config parameters in the command line carry over to manim's internal framework.
For example:

```bash
python -m manim_livestream -v WARNING

...INFO...

>>> config.verbosity
'WARNING'
>>>
```

- IPython is an option:

```bash
python -m manim_livestream --use-ipython

...INFO...

Python 3.9.2 (tags/v3.9.2:1a79785, Feb 19 2021, 13:44:55) [MSC v.1928 64 bit (AMD64)]
Type 'copyright', 'credits' or 'license' for more information
IPython 7.23.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]:

```

- Simple ways exist for simpler actions:

```py
Python 3.9.2 (tags/v3.9.2:1a79785, Feb 19 2021, 13:44:55) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.

>>> from manim_livestream import stream
>>> from manim import Circle, ShowCreation
>>> self = stream()
>>> circ = Circle()
>>> self.play(ShowCreation(circ))
```

- You want scenes present in files? Here you go:

```bash
python -m manim_livestream example_scenes/basic.py
Manim Community v0.6.0

1: OpeningManim
2: SquareToCircle
3: UpdatersExample
4: WarpSquare
5: WriteStuff

Choose number corresponding to desired scene/arguments.
(Use comma separated list for multiple entries)
Choice(s): 2

```

This particular one will render the scene and send the frames to the streaming protocol.

## Potential problems
- Last 2 or 3 frames don't get sent?
  Close the window and restart it with `open_client()`
- The entire thing freezes?
  Close the window and restart it with `open_client()`
- Using any other streaming protocol?
  As of yet, not a great plan. From experimentation rtp seems the most stable. However the
  streaming port shouldn't be too hard to modify.
  

## License and contribution
The code is released as Free Software under the [GNU/GPLv3](https://choosealicense.com/licenses/gpl-3.0/) license. 
Copying, adapting and republishing it is not only consent but also encouraged, particularly surrounding the subject of tests for the framework.

## Addendum
As long as the way Manim interprets scene compilation remains static, this library can easily be
used with any `manim>=0.6.0`_(as far as I know)_.

