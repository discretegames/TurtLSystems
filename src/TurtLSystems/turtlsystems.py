"""The core code of the TurtLSystems Python 3 package (https://pypi.org/project/TurtLSystems)."""

from typing import List, Dict, Tuple, Iterable, Optional, Union
import turtle

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
_INITIALIZED, _FINISHED = False, False


def clamp(value: int, minimum: int = 0, maximum: int = 255) -> int:
    """Clamps `value` between `minimum` and `maximum`."""
    return max(minimum, min(value, maximum))


def color_tuple(color: Iterable[int]) -> Tuple[int, int, int]:
    """Converts `color` to tuple with clamped rgb."""
    red, green, blue = zip(color, range(3))
    return clamp(red[0]), clamp(green[0]), clamp(blue[0])


def make_rules(rules: Union[str, Dict[str, str]]) -> Dict[str, str]:
    """Creates rules dict."""
    if isinstance(rules, str):
        split = rules.split()
        rules = {inp: out for inp, out in zip(split[::2], split[1::2])}
    return rules


def make_colors(color: Optional[Tuple[int, int, int]], fill_color: Optional[Tuple[int, int, int]],
                colors: Iterable[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """Creates colors list."""
    colors = list(map(color_tuple, colors))
    colors.extend(DEFAULT_COLORS[len(colors):])
    if color is not None:
        colors[0] = color_tuple(color)
    if fill_color is not None:
        colors[1] = color_tuple(fill_color)
    return colors


def lsystem(start: str, rules: Dict[str, str], level: int) -> str:
    """Iterates L-system initialzed to `start` based on `rules` `level` number of times."""
    for _ in range(level):
        start = ''.join(rules.get(c, c) for c in start)
    return start


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


def init(  # pylint: disable=too-many-arguments
    window_size: Tuple[Union[int, float], Union[int, float]] = (0.75, 0.75),
    window_title: str = "TurtLSystems",
    background_color: Tuple[int, int, int] = (0, 0, 0),
    background_image: Optional[str] = None,
    window_position: Tuple[Optional[int], Optional[int]] = (None, None),
    canvas_size: Tuple[Optional[int], Optional[int]] = (None, None),
    delay: int = 0,
    mode: str = 'standard'
) -> None:
    """TODO docstring"""
    if _FINISHED:
        print('Did not init() because finish() was already called.')
        return
    window_w, window_h = window_size
    window_x, window_y = window_position
    turtle.setup(window_w, window_h, window_x, window_y)
    # Use 1x1 canvas size unless canvas is actually bigger than window to avoid weird unnecessary scrollbars.
    # The canvas will still fill out the window, it won't behave like 1x1.
    canvas = turtle.getcanvas()  # Used to get final int window size as window_size may have been floats.
    canvas_w = 1 if canvas_size[0] is None or canvas_size[0] <= canvas.winfo_width() else canvas_size[0]
    canvas_h = 1 if canvas_size[1] is None or canvas_size[1] <= canvas.winfo_height() else canvas_size[1]
    turtle.screensize(canvas_w, canvas_h)
    turtle.title(window_title)
    turtle.mode(mode)
    turtle.delay(delay)
    turtle.colormode(255)
    turtle.bgcolor(color_tuple(background_color))
    turtle.bgpic(background_image)
    global _INITIALIZED  # pylint: disable=global-statement
    _INITIALIZED = True


# Dataclasses not in 3.6 and SimpleNamespace is not typed properly so use plain class for state.
class State:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """L-system state."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        position: Tuple[float, float],
        heading: float, angle: float,
        length: float,
        thickness: float,
        pen_color: Tuple[int, int, int],
        fill_color: Tuple[int, int, int],
        swap_signs: bool,
        modify_fill: bool
    ) -> None:
        self.position = position
        self.heading = heading
        self.angle = angle
        self.length = length
        self.thickness = thickness
        self.pen_color = pen_color
        self.fill_color = fill_color
        self.swap_signs = swap_signs
        self.change_fill = modify_fill


def run(  # pylint: disable=invalid-name,too-many-locals,too-many-branches,too-many-statements
    *,
    t: turtle.Turtle,
    string: str,
    colors: List[Tuple[int, int, int]],
    full_circle: float,
    angle: float,
    length: float,
    thickness: float,
    angle_increment: float,
    length_increment: float,
    length_scalar: float,
    thickness_increment: float,
    color_increments: Tuple[int, int, int]
) -> None:
    """Run turtle `t` on L-system string `string` with given options."""
    initial_angle, initial_length, initial_thickness = angle, length, thickness
    swap_signs, modify_fill = False, False
    pen_color, fill_color = colors[0], colors[1]
    stack: List[State] = []

    def set_pensize() -> None:
        t.pensize(max(0, thickness))

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
        color[channel] += (1 if decrement else -1) * color_increments[channel]
        set_color(color_tuple(color))

    set_pensize()
    t.pencolor(pen_color)
    t.fillcolor(fill_color)

    for c in string:  # pylint: disable=invalid-name
        # Length:
        if 'A' <= c <= 'Z':
            (t.pendown if t.pensize() else t.penup)()
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
            thickness = initial_thickness
            set_pensize()
        elif c == '>':
            thickness += thickness_increment
            set_pensize()
        elif c == '<':
            thickness -= thickness_increment
            set_pensize()
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
            stack.append(State((t.xcor(), t.ycor()), t.heading(), angle, length,
                               thickness, pen_color, fill_color, swap_signs, modify_fill))
        elif c == ']':
            if stack:
                state = stack.pop()
                orient(t, state.position, state.heading)
                angle, length = state.angle, state.length
                swap_signs, modify_fill = state.swap_signs, state.change_fill
                pen_color, fill_color = state.pen_color, state.fill_color
        elif c == '$':
            break


def draw(  # pylint: disable=too-many-locals,too-many-arguments
    start: str = 'F',
    rules: str = 'F F+F-F-F+F',
    level: int = 4,
    angle: float = 90,
    length: float = 10,
    thickness: float = 1,
    color: Optional[Tuple[int, int, int]] = (255, 255, 255),
    fill_color: Optional[Tuple[int, int, int]] = (128, 128, 128),
    background_color: Tuple[int, int, int] = (0, 0, 0),
    *,
    colors: Iterable[Tuple[int, int, int]] = DEFAULT_COLORS,
    position: Tuple[float, float] = (0, 0),
    heading: float = 0,
    angle_increment: float = 15,
    length_increment: float = 5,
    length_scalar: float = 2,
    thickness_increment: float = 1,
    red_increment: int = 4,
    green_increment: int = 4,
    blue_increment: int = 4,
    scale: float = 1,
    prefix: str = '',
    suffix: str = '',
    asap: bool = False,
    speed: Union[int, str] = 0,
    show_turtle: bool = False,
    turtle_shape: str = 'classic',
    full_circle: float = 360,
    finished: bool = True,
    exit_on_click: bool = True,
    skip_init: bool = False
) -> Optional[Tuple[str, Tuple[float, float], float]]:
    """TODO docstring"""
    if _FINISHED:
        print('Did not draw() because finish() was already called.')
        return None

    if not skip_init and not _INITIALIZED:
        init(background_color=background_color)
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

    run(t=t,
        string=string,
        colors=colors,
        full_circle=full_circle,
        angle=angle,
        length=scale*length,
        thickness=scale*thickness,
        angle_increment=angle_increment,
        length_increment=scale*length_increment,
        length_scalar=scale*length_scalar,
        thickness_increment=scale*thickness_increment,
        color_increments=(red_increment, green_increment, blue_increment))

    if asap:
        turtle.tracer(saved_tracer, saved_delay)
        turtle.update()
    if finished:
        finish(exit_on_click, skip_init)

    return string, (t.xcor(), t.ycor()), t.heading()


def finish(exit_on_click: bool = True, skip_init: bool = False) -> None:
    """Finish drawing and keep window open. Only needed if all calls to `draw` specified `finished=False`."""
    if not skip_init and not _INITIALIZED:
        init()
    global _FINISHED  # pylint: disable=global-statement
    if not _FINISHED:
        _FINISHED = True
        (turtle.exitonclick if exit_on_click else turtle.done)()


if __name__ == '__main__':
    draw()
    # setup(window_size=(1000 + 8, 300 + 8), canvas_size=(100, 100))
    # import time
    # time.sleep(1)
    # turtle.right(90)
    # turtle.color(255, 255, 128)
    # turtle.fd(1000)
    # import tkinter  # deiconify to shoe

    # canvas = turtle.getcanvas()
    # root: tkinter.Tk = turtle.Screen()._root  # type: ignore # pylint: disable=protected-access
    # print(canvas.canvasx(0), root.winfo_x())
    # x, y = root.winfo_x() + 12, root.winfo_y() + 35
    # w, h = root.winfo_width() - 8, root.winfo_height() - 8
    # print(root.winfo_vrootwidth(), root.winfo_width())
    # print(root.winfo_vrootx(), root.winfo_x())
    # from pyautogui import screenshot  # type: ignore
    # screenshot('out.png', region=(x, y, w, h))
    # print('done')
    # done()
    # init(window_size=(10, 30), canvas_size=(1000, 1000))
    # draw(last=False, color=(255, 100, 0), length=40, thickness=1)
    # draw(last=False, color=(255, 100, 0), length=40, thickness=15)
    # try:
    # except turtle.Terminator:
    #     print(999)
    #     exit()
    # canvas = turtle.getcanvas()._canvas
    # print(canvas.winfo_width())
    # # print(canvas.canvwidth, canvas.canvheight)
    # # print(type(canvas))
    # # input('wait')
    # canvas.postscript(file='out.eps')  # works for ps, needs to happen before done
    # import subprocess
    # # done()
    # subprocess.run(
    #     '''gswin64c -dSAFER -dBATCH -dNOPAUSE -dEPSCrop -r96 -sDEVICE=pngalpha -dGraphicsAlphaBits=4 -sOutputFile=output.png out.eps''')
    # # -g800x600
    #
# transparent=False, aliasing, png=None, gif=None, =1, ghostscript, padding=10, gif_padding=10, scale (applies to input dists), output_scale
