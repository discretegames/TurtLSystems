"""TurtLSystems examples, many from Wikipedia: https://en.wikipedia.org/wiki/L-system#Examples_of_L-systems

Try them by running this file and editing the comments at the bottom, or importing into your own file with:

from TurtLSystems.examples import *

Then calling the various functions:

sierpinski_triangle()
sierpinski_arrowhead()
square_koch_curve()
koch_snowflake()
koch_snowflake(anti=True)
dragon_curve()
cantor_set()
tree()
plant()
gradient()
"""

from typing import Tuple
from math import sqrt
from TurtLSystems import draw, wait, Exit


def sierpinski_triangle(level: int = 5, side_length: float = 300) -> None:
    """Draws a Sierpinski triangle with TurtLSystems."""
    length = side_length / (2**level)
    x, y = -side_length / 2, -side_length / (2 * 3**0.5)
    print(draw('F+G+G', 'F F+G-F-G+F G GG', level, 120, length,
               color=(255, 255, 0), asap=True, position=(x, y))[0])


def sierpinski_arrowhead(level: int = 5, side_length: float = 300) -> None:
    """Draws a Sierpinski arrowhead curve with TurtLSystems."""
    length = side_length / (2**level)
    x, y = -side_length / 2, -side_length / (2 * sqrt(3))
    print(draw('A', 'A B-A-B B A+B+A', level, 60, length, color=(255, 0, 0), asap=True,
               position=(x, y), heading=60 if level % 2 else 0)[0])


def koch_snowflake(level: int = 5, size: float = 300,  anti: bool = False,) -> None:
    """Draws a Koch snowflake with TurtLSystems."""
    length = size / (3**level)
    start = 'F++F++F' if anti else 'F--F--F'
    x, y = -size / 2, -size / (2 * sqrt(3))
    print(draw(start, 'F F+F--F+F', level, 60, length, color=(0, 0 if anti else 128, 255), asap=True,
               position=(x, y), heading=0 if anti else 60)[0])


def square_koch_curve(level: int = 5, width: float = 400) -> None:
    """Draws a square Koch curve with TurtLSystems."""
    length = width / (3**level)
    print(draw('F', 'F F+F-F-F+F', level, 90, length, color=(0, 255, 255), asap=True, position=(-width / 2, 0))[0])


def dragon_curve(level: int = 12, length: float = 5) -> None:
    """Draws a dragon curve with TurtLSystems."""
    print(draw('F', 'F F+G G F-G', level, 90, length, color=(255, 0, 255), asap=True)[0])


def cantor_set(level: int = 6, width: float = 729) -> None:
    """Draws a Cantor set with TurtLSystems."""
    print(draw('L', 'L D|d-/d-[L]dd[L]', level, 90, width, 1, asap=True,
               color=(255, 255, 255), length_scalar=3, position=(-width / 2, 0))[0])


def tree(level: int = 7, size: float = 200) -> None:
    """Draws a fractal binary tree with TurtLSystems."""
    length = size / 2**(level-1)
    print(draw('A', 'A B[-A]+A B BB', level, 45, length, color=(255, 128, 0), asap=True,
               position=(0, -size * 2**(level - 1)), heading=90)[0])


def plant(level: int = 5, size: float = 70) -> None:
    """Draws a fractal plant with TurtLSystems."""
    length = size / 2**(level-1)
    print(draw('X', 'X F+[[X]-X]-F[-FX]+X F FF', level, 20, length, color=(0, 255, 0), asap=True, heading=88)[0])


def gradient(color1: Tuple[int, int, int] = (255, 0, 0),
             color2: Tuple[int, int, int] = (0, 0, 255),
             size: int = 200) -> None:
    """Draws a gradient with TurtLSystems."""
    deltas = [(c1 - c2) / (size - 1) for c1, c2 in zip(color1, color2)]
    print(draw('s', 's l+f+s l *Y.:!|y/', size + 1, 90, 1,
               length_scalar=size, color=color1, asap=True, position=(-size/2, size/2),
               red_increment=deltas[0], green_increment=deltas[1], blue_increment=deltas[2])[0])


def dot(x: int = 0, y: int = 0) -> None:
    """Draws a dot with TurtLSystems."""
    print(draw('@', '', fill_color=(255, 255, 255), position=(x, y))[0])


if __name__ == '__main__':
    try:
        # Uncomment some of the following lines to see TurtLSystems in action:
        sierpinski_triangle()
        # sierpinski_arrowhead()
        # koch_snowflake()
        # koch_snowflake(anti=True)
        # square_koch_curve()
        # dragon_curve()
        # cantor_set()
        # tree()
        # plant()
        # gradient()

        dot()
        wait()
    except Exit:
        pass
