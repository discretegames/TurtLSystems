# pylint: skip-file
# type: ignore
# flake8: noqa

from TurtLSystems import *

draw('A', 'A B-A-B B A+B+A,', 5, 60, 7, 2, (200, 220, 255), None, (36, 8, 107),
     heading=60, red_increment=2, gif='examples/example.gif', max_frames=250, duration=30)

# draw('F+G+G', 'F F+G-F-G+F G GG', 5, 120, 10, color=(255, 255, 0), asap=True, png='examples/sierpinski')

# draw('A', 'A B-A-B B A+B+A', 5, 60, 10, color=(255, 0, 0), asap=True, heading=60, png='examples/arrowhead')

# draw('F--F--F', 'F F+F--F+F', 5, 60, 1.5, color=(0, 128, 255), asap=True, heading=60, png='examples/koch')

# draw('F++F++F', 'F F+F--F+F', 5, 60, 1.5, color=(0, 0, 255), asap=True, png='examples/antikoch')

# draw('F', 'F F+F-F-F+F', 5, 90, 3, color=(0, 255, 255), asap=True, png='examples/squarekoch')

# draw('F', 'F F+G G F-G', 12, 90, 5, color=(255, 0, 255), asap=True, png='examples/dragon')

# draw('A', 'A B[-A]+A B BB', 7, 45, 3, color=(255, 128, 0), asap=True, heading=90, png='examples/tree')

# draw('X', 'X F+[[X]-X]-F[-FX]+X F FF', 5, 20, 5, color=(0, 255, 0), asap=True, heading=88, png='examples/plant')

wait()
