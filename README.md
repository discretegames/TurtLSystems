# TurtLSystems

*In development. Project is still messy and not fully documented or tested.*

Python package for drawing [l-systems](https://en.wikipedia.org/wiki/L-system) with turtle graphics with options for png and gif output.

**<https://pypi.org/project/turtlsystems/>**

`pip install turtlsystems`

For png and gif output you need the ghostscript image converter: <https://ghostscript.com/>

Example and generating code:

![example](https://raw.githubusercontent.com/discretegames/turtlsystems/main/example.gif)

```py
from turtlsystems import init, draw
init((600, 600), background_color=(36, 8, 107))
draw('A', 'A B-A-B B A+B+A.', 60, 8, 5, 2, heading=150, position=(200, 00),
    color=(200, 220, 255), fill_color=(255, 255, 255), red_increment=-2, duration=30,
    gif='example.gif', max_frames=500, draws_per_frame=1, padding=10, fin=True, speed=10, asap=False)
```

commands inspired by <http://paulbourke.net/fractals/lsys>
