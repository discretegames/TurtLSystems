"""The core code of the TurtLSystems Python 3 package (https://pypi.org/project/TurtLSystems)."""

import os
import turtle
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Iterable, Optional, Union, cast
from tempfile import TemporaryDirectory
from contextlib import ExitStack
from PIL import Image
from packaging import version


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
PNG_EXT = '.png'
GIF_EXT = '.gif'
EPS_EXT = '.eps'
FINAL_NAME = 'final'
FRAME_NAME = 'frame{}'
DRAW_DIR_NAME = 'draw{}'
DPI = 96

_DRAW_NUMBER = 0
_INITIALIZED = False
_FINISHED = False
_GHOSTSCRIPT: Optional[str] = None


def clamp(value: int, minimum: int = 0, maximum: int = 255) -> int:
    """Clamps `value` between `minimum` and `maximum`."""
    return max(minimum, min(value, maximum))


def color_tuple(color: Iterable[int]) -> Tuple[int, int, int]:
    """Converts `color` to tuple with clamped rgb."""
    r, g, b = zip(color, range(3))
    return clamp(r[0]), clamp(g[0]), clamp(b[0])


def make_rules(rules: Union[str, Dict[str, str]]) -> Dict[str, str]:
    """Creates rules dict."""
    if isinstance(rules, str):
        split = rules.split()
        rules = dict(zip(split[::2], split[1::2]))
    return rules


def make_colors(color: Optional[Tuple[int, int, int]], fill_color: Optional[Tuple[int, int, int]],
                colors: Iterable[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """Creates colors list."""
    colors = list(map(color_tuple, colors))
    colors.extend(DEFAULT_COLORS[len(colors):])
    if color:
        colors[0] = color_tuple(color)
    if fill_color:
        colors[1] = color_tuple(fill_color)
    return colors


def make_drawdir(tmpdir: str) -> Path:
    """Creates drawdir in tempdir labeled with current draw number."""
    drawdir = Path(tmpdir).resolve() / DRAW_DIR_NAME.format(_DRAW_NUMBER)
    drawdir.mkdir(parents=True, exist_ok=True)
    for file in drawdir.iterdir():
        if file.is_file():
            file.unlink(missing_ok=True)
    return drawdir


def lsystem(start: str, rules: Dict[str, str], level: int) -> str:
    """Iterates L-system initialzed to `start` based on `rules` `level` number of times."""
    for _ in range(level):
        start = ''.join(rules.get(c, c) for c in start)
    return start


def orient(t: turtle.Turtle, position: Tuple[float, float], heading: float) -> None:
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


def get_background_color() -> Tuple[int, int, int]:
    """Returns current turtle graphics background color. Assumes it's a 0-255 tuple."""
    r, g, b = turtle.bgcolor()
    return int(r), int(g), int(b)


def guess_ghostscript(ghostscript: Optional[str] = None) -> str:
    """Guess the path to ghostscript if it's not already set. Only guesses well on Windows.
    Should prevent people from needing to add ghostscript to PATH.
    """
    if ghostscript:
        return ghostscript
    if os.name != 'nt':
        return 'gs'  # I'm not sure where to look on non-Windows OSes so just guess "gs".
    locations = "C:\\Program Files\\gs", "C:\\Program Files (x86)\\gs"
    files = 'gswin64c.exe', 'gswin32c.exe', 'gs.exe'
    for location in locations:
        path = Path(location)
        if path.exists():
            versions = [v for v in path.iterdir() if v.is_dir() and v.name.startswith('gs')]
            versions.sort(key=lambda v: version.parse(v.name[2:]), reverse=True)
            for v in versions:
                for file in files:
                    exe = v / 'bin' / file
                    if exe.exists():
                        print(f'Found ghostscript at "{exe}".')
                        return str(exe)
    return 'gswin64c'  # Last ditch guess.


def init(
    window_size: Tuple[Union[int, float], Union[int, float]] = (0.75, 0.75),
    window_title: str = "TurtLSystems",
    background_color: Tuple[int, int, int] = (0, 0, 0),
    background_image: Optional[str] = None,
    window_position: Tuple[Optional[int], Optional[int]] = (None, None),
    canvas_size: Tuple[Optional[int], Optional[int]] = (None, None),
    delay: int = 0,
    mode: str = 'standard',
    ghostscript: Optional[str] = None
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
    global _GHOSTSCRIPT, _INITIALIZED
    _GHOSTSCRIPT = guess_ghostscript(ghostscript)
    _INITIALIZED = True


# Dataclasses not in 3.6 and SimpleNamespace is not typed properly so use plain class for state.
class State:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """L-system state."""

    def __init__(
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


def run(  # pylint: disable=too-many-branches,too-many-statements
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
    color_increments: Tuple[int, int, int],
    gif: Optional[str],
    draws_per_frame: int,
    max_frames: int,
    drawdir: Optional[Path]
) -> List[Tuple[str, Tuple[int, int], Tuple[int, int, int]]]:
    """Run turtle `t` on L-system string `string` with given options."""
    initial_angle, initial_length, initial_thickness = angle, length, thickness
    swap_signs, modify_fill = False, False
    pen_color, fill_color = colors[0], colors[1]
    stack: List[State] = []
    gif_data: List[Tuple[str, Tuple[int, int], Tuple[int, int, int]]] = []
    draws, frames_attempted = 0, 0

    def save_frame() -> None:
        nonlocal frames_attempted
        frames_attempted += 1
        if len(gif_data) < max_frames:
            eps = str((cast(Path, drawdir) / FRAME_NAME.format(len(gif_data))).with_suffix(EPS_EXT))
            gif_data.append((eps, save_eps(eps), get_background_color()))

    def gif_handler() -> None:
        if gif:
            nonlocal draws
            draws += 1
            if draws % draws_per_frame == 0:
                save_frame()

    def set_pensize() -> None:
        t.pensize(max(0, thickness))  # type: ignore

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
    if gif:
        save_frame()

    for c in string:
        # Length:
        if 'A' <= c <= 'Z':
            (t.pendown if t.pensize() else t.penup)()
            t.forward(length)
            gif_handler()
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
            gif_handler()
        elif c == '@':
            t.dot(None, fill_color)
            gif_handler()
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

    if gif:
        if draws % draws_per_frame != 0:
            save_frame()  # Save frame of final changes unless nothing has changed.
        print(f'Prepped {len(gif_data)} gif frames of {frames_attempted} attempted for {draws + 1} draws.')

    return gif_data


def draw(
    start: str = 'F',
    rules: str = 'F F+F-F-F+F',
    angle: float = 90,
    length: float = 10,
    level: int = 4,
    thickness: float = 1,
    color: Optional[Tuple[int, int, int]] = (255, 255, 255),
    fill_color: Optional[Tuple[int, int, int]] = (128, 128, 128),
    background_color: Optional[Tuple[int, int, int]] = None,
    *,
    colors: Iterable[Tuple[int, int, int]] = DEFAULT_COLORS,
    position: Tuple[float, float] = (0, 0),
    heading: float = 0,
    angle_increment: float = 15,
    length_increment: float = 5,
    length_scalar: float = 2,
    thickness_increment: float = 1,
    red_increment: int = 1,
    green_increment: int = 1,
    blue_increment: int = 1,
    scale: float = 1,
    prefix: str = '',
    suffix: str = '',
    asap: bool = False,
    speed: Union[int, str] = 0,
    show_turtle: bool = False,
    turtle_shape: str = 'classic',
    full_circle: float = 360,
    fin: bool = True,
    exit_on_click: bool = True,
    skip_init: bool = False,
    png: Optional[str] = None,
    padding: Optional[int] = 10,
    output_scale: float = 1,
    antialiasing: int = 4,
    transparent: bool = False,
    gif: Optional[str] = None,
    draws_per_frame: int = 1,
    max_frames: int = 100,
    duration: int = 20,
    wait: int = 500,
    delay: int = 0,
    loops: Optional[int] = None,
    reverse: bool = False,
    alternate: bool = False,
    optimize: bool = True,
    tmpdir: Optional[str] = None
) -> Optional[Tuple[str, Tuple[float, float], float]]:
    """TODO docstring"""
    global _DRAW_NUMBER
    _DRAW_NUMBER += 1
    if _FINISHED:
        print('Did not draw() because finish() was already called.')
        return None

    if not skip_init and not _INITIALIZED:
        init()
    turtle.colormode(255)
    if background_color:
        turtle.bgcolor(background_color)
    if asap:
        saved_tracer, saved_delay = turtle.tracer(), turtle.delay()
        turtle.tracer(0, 0)

    t = turtle.Turtle()
    t.degrees(full_circle)
    t.speed(speed)
    t.shape(turtle_shape)
    if show_turtle:
        t.showturtle()
    else:
        t.hideturtle()
    position = scale * position[0], scale * position[1]
    orient(t, position, heading)

    string = prefix + lsystem(start, make_rules(rules), level) + suffix
    colors = make_colors(color, fill_color, colors)

    with ExitStack() as exit_stack:
        if png or gif:
            save_gif_pngs = True
            if not tmpdir:
                tmpdir = exit_stack.enter_context(TemporaryDirectory())
                save_gif_pngs = False
            drawdir = make_drawdir(tmpdir)

        gif_data = run(t=t,
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
                       color_increments=(red_increment, green_increment, blue_increment),
                       gif=gif,
                       draws_per_frame=draws_per_frame,
                       max_frames=max_frames,
                       drawdir=drawdir if gif else None)
        if png:
            eps = str((drawdir / FINAL_NAME).with_suffix(EPS_EXT))
            png, _, _ = save_png(png, eps, save_eps(eps), output_scale, antialiasing,
                                 get_background_color(), padding, transparent)
            print(f'Saved png "{png}".')

        if gif:
            gif = save_gif(gif, gif_data, output_scale, antialiasing, padding, transparent,
                           duration, wait, delay, loops, reverse, alternate, optimize, save_gif_pngs)
            print(f'Saved gif "{gif}".')

        if asap:
            turtle.tracer(saved_tracer, saved_delay)
            turtle.update()

    if fin:
        finish(exit_on_click, skip_init)

    return string, (t.xcor(), t.ycor()), t.heading()


def save_eps(eps: str) -> Tuple[int, int]:
    """TODO docstring"""
    turtle.update()
    canvas = turtle.getcanvas()
    width = max(canvas.winfo_width(), canvas.canvwidth)  # type: ignore
    height = max(canvas.winfo_height(), canvas.canvheight)  # type: ignore
    canvas.postscript(file=eps, x=-width//2, y=-height//2, width=width, height=height)  # type: ignore
    return width, height


def save_png(
    png: str,
    eps: str,
    size: Tuple[int, int],
    output_scale: float,
    antialiasing: int,
    background_color: Tuple[int, int, int],
    padding: Optional[int],
    transparent: bool,
    rect: Optional[Tuple[int, int, int, int]] = None,
    resave: bool = True,
) -> Tuple[str, Image.Image, Optional[Tuple[int, int, int, int]]]:
    """TODO docstring"""
    png = str(Path(png).with_suffix(PNG_EXT).resolve())
    eps_to_png(eps, png, size, output_scale, antialiasing)
    image = Image.open(png).convert('RGBA')
    if padding is not None:
        if rect is None:
            rect = get_padding_rect(image, round(output_scale * padding))
        image = image.crop(rect)
    background = Image.new('RGBA', image.size, background_color + ((0,) if transparent else (255,)))
    image = Image.alpha_composite(background, image)
    if resave:
        image.save(png)
    return png, image, rect


def save_gif(
    gif: str,
    gif_data: List[Tuple[str, Tuple[int, int], Tuple[int, int, int]]],
    output_scale: float,
    antialiasing: int,
    padding: Optional[int],
    transparent: bool,
    duration: int,
    wait: int,
    delay: int,
    loops: Optional[int],
    reverse: bool,
    alternate: bool,
    optimize: bool,
    save_gif_pngs: bool
) -> str:
    """TODO docstring"""
    rect = None
    images = []
    for i, (eps, size, bg) in enumerate(reversed(gif_data)):  # Reverse so rect corresponds to last frame.
        png = str(Path(eps).with_suffix(PNG_EXT))
        _, image, r = save_png(png, eps, size, output_scale, antialiasing,
                               bg, padding, transparent, rect, save_gif_pngs)
        images.append(image)
        if rect is None:
            rect = r
            print(f'Making {len(gif_data)} gif frames..', end='', flush=True)
        elif (len(gif_data) - i) % 10 == 0:
            print(f'{len(gif_data) - i}..', end='', flush=True)
    print('.')
    if not reverse:
        images.reverse()  # Reversing here puts it back in proper order.
    if alternate:
        images.extend(images[-2:0:-1])
    gif = str(Path(gif).with_suffix(GIF_EXT).resolve())
    delaying = [images[0]] * (max(0, delay - duration) // duration)
    waiting = [images[-1]] * (max(0, wait - duration) // duration)
    frames = delaying + images[1:] + waiting
    images[0].save(gif, save_all=True, append_images=frames, loop=loops or 0, duration=duration,
                   optimize=optimize, transparency=0 if transparent else 255)
    # PIL seems to treat blank animated gifs like static gifs, so their timing is wrong. But nbd since they're blank.
    return gif


def eps_to_png(eps: str, png: str, size: Tuple[int, int], output_scale: float, antialiasing: int) -> None:
    """TODO docstring"""
    global _GHOSTSCRIPT
    _GHOSTSCRIPT = guess_ghostscript(_GHOSTSCRIPT)  # Re-get ghostscript just in case init was never called.
    result = subprocess.run([_GHOSTSCRIPT,
                             '-q',
                            '-dSAFER',
                             '-dBATCH',
                             '-dNOPAUSE',
                             '-dEPSCrop',
                             '-sDEVICE=pngalpha',
                             f'-r{round(DPI * output_scale)}',
                             f'-g{round(output_scale * size[0])}x{round(output_scale * size[1])}',
                             f'-dGraphicsAlphaBits={antialiasing}',
                             f'-sOutputFile={png}',
                             eps],
                            check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    if result.returncode:
        print(result.stdout)


def get_padding_rect(image: Image.Image, padding: int) -> Tuple[int, int, int, int]:
    """TODO docstring"""
    print(f'Padding {image.width}x{image.height} pixel image...')
    x_min, y_min, x_max, y_max = image.width - 1, image.height - 1, 0, 0
    data = image.load()
    empty = True
    for y in range(image.height):
        for x in range(image.width):
            if data[x, y][3] != 0:
                empty = False
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)
    if empty:
        x_min = x_max = image.width//2
        y_min = y_max = image.height//2
    x_min -= padding
    y_min -= padding
    x_max = max(x_max + padding, x_min) + 1
    y_max = max(y_max + padding, y_min) + 1
    return x_min, y_min, x_max, y_max


def finish(exit_on_click: bool = True, skip_init: bool = False) -> None:
    """Finish drawing and keep window open. Only needed if all calls to `draw` specified `fin=False`."""
    if not skip_init and not _INITIALIZED:
        init()
    global _FINISHED
    if not _FINISHED:
        _FINISHED = True
        (turtle.exitonclick if exit_on_click else turtle.done)()


if __name__ == '__main__':
    init((600, 600), background_color=(36, 8, 107))
    st = "F-G-G"
    ru = "F {F-G+F+G-F G @GG"
    draw('A', 'A B-A-B B A+B+A.', 60, 8, 5, 2, heading=150, position=(200, 00),
         color=(200, 220, 255), fill_color=(255, 255, 255), red_increment=-2,
         gif='tri', max_frames=500, draws_per_frame=1, alternate=False,
         padding=10, fin=True, speed=10, asap=False, reverse=False, tmpdir='', show_turtle=False,
         turtle_shape='turtle', duration=30)

