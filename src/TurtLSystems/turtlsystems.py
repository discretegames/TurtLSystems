"""The core code of the TurtLSystems Python 3 package (https://pypi.org/project/TurtLSystems)."""

from typing import List, Dict, Tuple, Iterable, Optional, Union
import turtle

IS_SETUP = False
IS_DONE = False
DEFAULT_COLORS = (
    (255, 255, 255),
    (128, 128, 128),
    (255, 0, 0),
    (255, 128, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (128, 0, 255),
    (255, 0, 255),
)


def make_rules(rules: Union[str, Dict[str, str]]) -> Dict[str, str]:
    """Creates rules dict."""
    if isinstance(rules, str):
        split = rules.split()
        rules = {inp: out for inp, out in zip(split[::2], split[1::2])}
    return rules


def make_colors(color: Optional[Tuple[int, int, int]], fill_color: Optional[Tuple[int, int, int]],
                colors: Iterable[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """Creates colors list."""
    colors = list(map(tuple, colors))  # type: ignore
    colors.extend(DEFAULT_COLORS[len(colors):])
    if color is not None:
        colors[0] = tuple(color)  # type: ignore
    if fill_color is not None:
        colors[1] = tuple(fill_color)  # type: ignore
    return colors


def orient(t: turtle.Turtle, position: Tuple[float, float], heading: float) -> None:  # pylint: disable=invalid-name
    """Silently orients turtle `t` to given `position` and `heading`."""
    speed = t.speed()
    down = t.isdown()
    t.penup()
    t.speed(0)
    t.setposition(position)
    t.setheading(heading)
    t.speed(speed)
    if down:
        t.pendown()


def lsystem(start: str, rules: Dict[str, str], level: int) -> str:
    """Iterates L-system initialzed to `start` based on `rules` `level` number of times."""
    for _ in range(level):
        start = ''.join(rules.get(c, c) for c in start)
    return start


def done() -> None:
    """Finalize TurtLSystems drawing. Only needed if all calls to `draw` specified `last=False`."""
    global IS_DONE  # pylint: disable=global-statement
    if not IS_DONE:
        IS_DONE = True
        turtle.done()


def setup(title: str = "TurtLSystems",  # pylint: disable=too-many-arguments
          window_size: Tuple[Union[int, float], Union[int, float]] = (0.75, 0.75),
          background_color: Tuple[int, int, int] = (0, 0, 0),
          background_image: Optional[str] = None,
          canvas_size: Tuple[Optional[int], Optional[int]] = (None, None),
          window_position: Tuple[Optional[int], Optional[int]] = (None, None),
          delay: int = 0,
          mode: str = 'standard') -> None:
    """TODO docstring"""
    turtle.colormode(255)
    turtle.title(title)
    turtle.mode(mode)
    turtle.delay(delay)
    window_w, window_h = window_size
    window_x, window_y = window_position
    turtle.setup(window_w, window_h, window_x, window_y)
    canvas_w, canvas_h = canvas_size
    turtle.screensize(canvas_w, canvas_h)  # type: ignore
    turtle.bgcolor(background_color)
    turtle.bgpic(background_image)
    global IS_SETUP  # pylint: disable=global-statement
    IS_SETUP = True


class State:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """TODO Docstring"""
    # pylint: disable=too-many-arguments

    def __init__(self,
                 position: Tuple[float, float],
                 heading: float, angle: float,
                 length: float,
                 thickness: int,
                 pen_color: Tuple[int, int, int],
                 fill_color: Tuple[int, int, int],
                 swap_signs: bool,
                 modify_fill: bool) -> None:
        self.position = position
        self.heading = heading
        self.angle = angle
        self.length = length
        self.thickness = thickness
        self.pen_color = pen_color
        self.fill_color = fill_color
        self.swap_signs = swap_signs
        self.change_fill = modify_fill


def run(t: turtle.Turtle,  # pylint: disable=invalid-name,too-many-locals,too-many-branches,too-many-statements
        string: str, *,
        colors: List[Tuple[int, int, int]],
        full_circle: float,
        angle: float,
        length: float,
        thickness: int,
        angle_increment: float,
        length_increment: float,
        length_scalar: float,
        thickness_increment: int,
        color_increments: Tuple[int, int, int]) -> None:
    """Run turtle `t` on L-system string `string` with given options."""
    initial_angle, initial_length = angle, length
    swap_signs, modify_fill = False, False
    pen_color, fill_color = colors[0], colors[1]
    t.pencolor(pen_color)
    t.fillcolor(fill_color)
    stack: List[State] = []

    def set_color(color: Tuple[int, int, int]) -> None:
        nonlocal pen_color, fill_color, modify_fill
        if modify_fill:
            modify_fill = False
            fill_color = color
            t.fillcolor(fill_color)
        else:
            pen_color = color
            t.pencolor(pen_color)

    def increment_color(channel: int, decrement: bool = False) -> None:
        color = list(fill_color if modify_fill else pen_color)
        amount = (1 if decrement else -1) * color_increments[channel]
        color[channel] = max(0, min(color[channel] + amount, 255))
        set_color(tuple(color))  # type: ignore

    for c in string:  # pylint: disable=invalid-name
        # Length:
        if 'A' <= c <= 'Z':
            t.pendown()
            t.forward(length)
        elif 'a' <= c <= 'z':
            t.penup()
            t.forward(length)
        elif c == '_':
            length = initial_length
        elif c == '^':
            length += length_increment
        elif c == '%':
            length -= length_increment
        elif c == '*':
            length *= length_scalar
        elif c == '/':
            length /= length_scalar
        # Angle:
        elif c == '+':
            (t.right if swap_signs else t.left)(angle)
        elif c == '-':
            (t.left if swap_signs else t.right)(angle)
        elif c == '&':
            swap_signs = not swap_signs
        elif c == '|':
            t.right(full_circle/2.0)
        elif c == '~':
            angle = initial_angle
        elif c == ')':
            angle += angle_increment
        elif c == '(':
            angle -= angle_increment
        # Thickness:
        elif c == '=':
            t.pensize(thickness)
        elif c == '>':
            t.pensize(max(1, thickness + thickness_increment))
        elif c == '<':
            t.pensize(max(1, thickness - thickness_increment))
        # Color:
        elif '0' <= c <= '9':
            set_color(colors[int(c)])
        elif c == '#':
            modify_fill = True
        elif c == ',':
            increment_color(0)
        elif c == '.':
            increment_color(0, True)
        elif c == ';':
            increment_color(1)
        elif c == ':':
            increment_color(1, True)
        elif c == '?':
            increment_color(2)
        elif c == '!':
            increment_color(2, True)
        # Other:
        elif c == '{':
            t.begin_fill()
        elif c == '}':
            t.end_fill()
        elif c == '@':
            t.dot(None, fill_color)
        elif c == '`':
            stack.clear()
        elif c == '[':
            stack.append(State((t.xcor(), t.ycor()), t.heading(), angle, length, thickness,
                         pen_color, fill_color, swap_signs, modify_fill))
        elif c == ']':
            if stack:
                state = stack.pop()
                orient(t, state.position, state.heading)
                angle, length = state.angle, state.length
                swap_signs, modify_fill = state.swap_signs, state.change_fill
                pen_color, fill_color = state.pen_color, state.fill_color
        elif c == '$':
            break


def draw(start: str = 'F',  # pylint: disable=too-many-locals,too-many-arguments
         rules: str = 'F F+F-F-F+F',
         level: int = 4,
         angle: float = 90,
         length: float = 10,
         thickness: int = 1,
         color: Optional[Tuple[int, int, int]] = (255, 255, 255),
         fill_color: Optional[Tuple[int, int, int]] = (128, 128, 128),
         background_color: Tuple[int, int, int] = (0, 0, 0), *,
         colors: Iterable[Tuple[int, int, int]] = DEFAULT_COLORS,
         angle_increment: float = 15,
         length_increment: float = 5,
         length_scalar: float = 2,
         thickness_increment: int = 1,
         red_increment: int = 4,
         green_increment: int = 4,
         blue_increment: int = 4,
         position: Tuple[float, float] = (0, 0),
         heading: float = 0,
         speed: Union[int, str] = 0,
         asap: bool = False,
         prefix: str = '',
         suffix: str = '',
         show_turtle: bool = False,
         turtle_shape: str = 'classic',
         full_circle: float = 360,
         last: bool = True,) -> Tuple[str, Tuple[float, float], float]:
    """TODO docstring"""
    if not IS_SETUP:
        setup()

    turtle.colormode(255)
    turtle.bgcolor(background_color)
    if asap:
        saved_tracer, saved_delay = turtle.tracer(), turtle.delay()
        turtle.tracer(0, 0)

    t = turtle.Turtle()  # pylint: disable=invalid-name
    t.degrees(full_circle)
    t.speed(speed)
    t.shape(turtle_shape)
    if show_turtle:
        t.showturtle()
    else:
        t.hideturtle()
    orient(t, position, heading)

    string = prefix + lsystem(start, make_rules(rules), level) + suffix
    colors = make_colors(color, fill_color, colors)

    run(t, string,
        colors=colors,
        full_circle=full_circle,
        angle=angle,
        length=length,
        thickness=thickness,
        angle_increment=angle_increment,
        length_increment=length_increment,
        length_scalar=length_scalar,
        thickness_increment=thickness_increment,
        color_increments=(red_increment, green_increment, blue_increment))

    if asap:
        turtle.tracer(saved_tracer, saved_delay)
        turtle.update()
    if last:
        done()

    return string, (t.xcor(), t.ycor()), t.heading()


if __name__ == '__main__':
    draw()
