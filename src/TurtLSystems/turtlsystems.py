"""Core source code of turtlsystems Python 3 package (https://pypi.org/project/turtlsystems)."""

import os
import turtle
import subprocess
from pathlib import Path
from typing import Any, List, Dict, Tuple, Iterable, Sequence, Optional, Union, cast
from tempfile import TemporaryDirectory
from contextlib import ExitStack
from PIL import Image
from packaging import version

# Types:
Color = Tuple[int, int, int]
OpColor = Optional[Color]

# Globals:
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
PNG_EXT, GIF_EXT, EPS_EXT = '.png', '.gif', '.eps'
FINAL_NAME, FRAME_NAME, DRAW_DIR_NAME = 'final', 'frame{}', 'draw{}'
DPI = 96

# Mutating globals:
_DRAW_NUMBER = 0
_INITIALIZED = _WAITED = _SILENT = False
_GHOSTSCRIPT = ''


# Dataclasses are not in 3.6 and SimpleNamespace is not typed properly so decided to use a plain class for State.
class State:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """L-system state."""

    def __init__(
        self,
        position: Tuple[float, float],
        heading: float, angle: float,
        length: float,
        thickness: float,
        pen_color: OpColor,
        fill_color: OpColor,
        swap_signs: bool,
        swap_cases: bool,
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
        self.swap_cases = swap_cases
        self.modify_fill = modify_fill


#####################
# Package Functions #
#####################


def init(
    window_size: Tuple[Union[int, float], Union[int, float]] = (0.75, 0.75),
    window_title: str = "TurtLSystems",
    background_color: Tuple[int, int, int] = (0, 0, 0),
    background_image: Optional[str] = None,
    window_position: Tuple[Optional[int], Optional[int]] = (None, None),
    canvas_size: Tuple[Optional[int], Optional[int]] = (None, None),
    delay: int = 0,
    mode: str = 'standard',
    ghostscript: Optional[str] = None,
    silent: bool = False
) -> None:
    """TODO docstring"""
    global _SILENT, _GHOSTSCRIPT, _INITIALIZED
    _SILENT = silent
    if _WAITED:
        message('Did not init() because wait() was already called.')
        return
    _GHOSTSCRIPT = ghostscript or ''
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
    turtle.bgcolor(background_color)
    turtle.bgpic(background_image)
    _INITIALIZED = True


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
    colors: Optional[Iterable[Optional[Tuple[int, int, int]]]] = None,
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
    hold: int = 500,
    delay: int = 0,
    loops: Optional[int] = None,
    reverse: bool = False,
    alternate: bool = False,
    optimize: bool = True,
    tmpdir: Optional[str] = None
) -> Optional[Tuple[str, turtle.Turtle]]:
    """TODO docstring"""
    global _DRAW_NUMBER
    _DRAW_NUMBER += 1
    if _WAITED:
        message('Did not draw() because wait() was already called.')
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

    with ExitStack() as exit_stack:
        if png or gif:
            save_gif_pngs = True
            if not tmpdir:
                tmpdir = exit_stack.enter_context(TemporaryDirectory())
                save_gif_pngs = False
            drawdir = make_drawdir(tmpdir)
            global _GHOSTSCRIPT
            if not _GHOSTSCRIPT:
                _GHOSTSCRIPT = guess_ghostscript()
                message(f'Guessed ghostscript to be "{_GHOSTSCRIPT}".')

        gif_data = run(t=t,
                       string=string,
                       colors=make_colors(color, fill_color, colors),
                       full_circle=full_circle,
                       position=position,
                       heading=heading,
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
            try:
                png, _, _ = save_png(png, eps, save_eps(eps), output_scale, antialiasing,
                                     get_background_color(), padding, transparent)
                message(f'Saved png "{png}".')
            except Exception as e:  # pylint: disable=broad-except
                message('Unable to save png:', e)

        if gif:
            try:
                gif = save_gif(gif, gif_data, output_scale, antialiasing, padding, transparent,
                               duration, hold, delay, loops, reverse, alternate, optimize, save_gif_pngs)
                message(f'Saved gif "{gif}".')
            except Exception as e:  # pylint: disable=broad-except
                message('Unable to save gif:', e)

        if asap:
            turtle.tracer(saved_tracer, saved_delay)
            turtle.update()

    return string, t


def wait(exit_on_click: bool = True, *, skip_init: bool = False) -> None:
    """Use `wait()` after all calls to `draw(...)` to keep the window open.

    Args:
        `exit_on_click=True` (bool): Whether the window can be closed by clicking anywhere.
        `skip_init=False` (bool): For advanced use. Whether to skip calling `init`.
    """
    if not skip_init and not _INITIALIZED:
        init()
    global _WAITED
    if not _WAITED:
        _WAITED = True
        (turtle.exitonclick if exit_on_click else turtle.done)()


####################
# Helper Functions #
####################


def message(*args: Any, **kwargs: Any) -> None:
    """Alias for `print` but only runs when not silenced."""
    if not _SILENT:
        print(*args, **kwargs)


def lsystem(start: str, rules: Dict[str, str], level: int) -> str:
    """Iterates L-system initialzed to `start` based on `rules` `level` number of times."""
    for _ in range(level):
        start = ''.join(rules.get(c, c) for c in start)
    return start


def clamp(value: int, minimum: int = 0, maximum: int = 255) -> int:
    """Clamps `value` between `minimum` and `maximum`."""
    return max(minimum, min(value, maximum))


def conform_color(color: Optional[Sequence[int]]) -> OpColor:
    """Ensures `color` is a tuple with 0-255 clamped rgb."""
    if color:
        return clamp(int(color[0])), clamp(int(color[1])), clamp(int(color[2]))
    return None


def get_background_color() -> Color:
    """Returns current turtle graphics background color. Assumes it's a 0-255 rgb tuple."""
    r, g, b = turtle.bgcolor()
    return int(r), int(g), int(b)


def make_rules(rules: Union[str, Dict[str, str]]) -> Dict[str, str]:
    """Creates rules dict."""
    if isinstance(rules, str):
        split = rules.split()
        rules = dict(zip(split[::2], split[1::2]))
    return rules


def make_colors(color: OpColor, fill_color: OpColor, colors: Optional[Iterable[OpColor]]) -> Tuple[OpColor, ...]:
    """Creates final colors tuple."""
    if colors is None:
        return conform_color(color), conform_color(fill_color), *DEFAULT_COLORS[2:]
    colors = [conform_color(c) for c, _ in zip(colors, range(len(DEFAULT_COLORS)))]
    colors.extend(DEFAULT_COLORS[len(colors):])
    return tuple(colors)


def make_drawdir(tmpdir: str) -> Path:
    """Creates drawdir in tempdir labeled with current draw number."""
    drawdir = Path(tmpdir).resolve() / DRAW_DIR_NAME.format(_DRAW_NUMBER)
    drawdir.mkdir(parents=True, exist_ok=True)
    for file in drawdir.iterdir():
        if file.is_file():
            file.unlink(missing_ok=True)
    return drawdir


def orient(t: turtle.Turtle, position: Optional[Tuple[float, float]], heading: Optional[float]) -> None:
    """Silently orients turtle `t` to given `position` and `heading`."""
    speed = t.speed()
    down = t.isdown()
    t.penup()
    t.speed(0)
    if position:
        t.setposition(position)
    if heading is not None:
        t.setheading(heading)
    t.speed(speed)
    if down:
        t.pendown()


def guess_ghostscript() -> str:
    """Guess the path to ghostscript. Only guesses well on Windows.
    Should prevent people from needing to add ghostscript to PATH.
    """
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
                        return str(exe)
    return 'gswin64c'  # Last ditch guess.


def eps_to_png(eps: str, png: str, size: Tuple[int, int], output_scale: float, antialiasing: int) -> None:
    """TODO docstring"""
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
                             f'-dTextAlphaBits={antialiasing}',
                             f'-sOutputFile={png}',
                             eps],
                            check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    if result.returncode:
        message(f'Ghostscript ({_GHOSTSCRIPT}) exit code {result.returncode}:')
        message(result.stdout)


def get_padding_rect(image: Image.Image, padding: int) -> Tuple[int, int, int, int]:
    """TODO docstring"""
    message(f'Padding {image.width}x{image.height} pixel image...')
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
    background_color: Color,
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
    gif_data: List[Tuple[str, Tuple[int, int], Color]],
    output_scale: float,
    antialiasing: int,
    padding: Optional[int],
    transparent: bool,
    duration: int,
    hold: int,
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
        if not i:
            rect = r
            message(f'Making {len(gif_data)} gif frames..', end='', flush=True)
        elif (len(gif_data) - i) % 10 == 0:
            message(f'{len(gif_data) - i}..', end='', flush=True)
    message('.')
    if not reverse:
        images.reverse()  # Reversing here puts it back in proper order.
    if alternate:
        images.extend(images[-2:0:-1])
    gif = str(Path(gif).with_suffix(GIF_EXT).resolve())
    delaying = [images[0]] * (max(0, delay - duration) // duration)
    holding = [images[-1]] * (max(0, hold - duration) // duration)
    frames = delaying + images[1:] + holding
    images[0].save(gif, save_all=True, append_images=frames, loop=loops or 0, duration=duration,
                   optimize=optimize, transparency=0 if transparent else 255)
    # PIL seems to treat blank animated gifs like static gifs, so their timing is wrong. But nbd since they're blank.
    return gif


def run(  # pylint: disable=too-many-branches,too-many-statements
    *,
    t: turtle.Turtle,
    string: str,
    colors: Tuple[OpColor, ...],
    full_circle: float,
    position: Tuple[float, float],
    heading: float,
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
) -> List[Tuple[str, Tuple[int, int], Color]]:
    """Run turtle `t` on L-system string `string` with given options."""
    initial_angle, initial_length, initial_thickness = angle, length, thickness
    swap_signs, swap_cases, modify_fill = False, False, False
    pen_color, fill_color = colors[0], colors[1]
    stack: List[State] = []
    gif_data: List[Tuple[str, Tuple[int, int], Color]] = []
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

    def set_color(color: OpColor) -> None:
        nonlocal pen_color, fill_color, modify_fill
        if modify_fill:
            modify_fill = False
            fill_color = color
            if fill_color:
                t.fillcolor(fill_color)
        else:
            pen_color = color
            if pen_color:
                t.pencolor(pen_color)

    def increment_color(channel: int, decrement: bool = False) -> None:
        color = fill_color if modify_fill else pen_color
        if color:
            amount = (-1 if decrement else 1) * color_increments[channel]
            lst = list(color)
            lst[channel] = clamp(lst[channel] + amount)
            set_color((lst[0], lst[1], lst[2]))

    set_pensize()
    if pen_color:
        t.pencolor(pen_color)
    if fill_color:
        t.fillcolor(fill_color)
    if gif:
        save_frame()

    for c in string:
        if swap_cases and c.isalpha():
            c = c.lower() if c.isupper() else c.upper()

        # Length:
        if 'A' <= c <= 'Z':
            if pen_color and t.pensize():
                t.pendown()
            else:
                t.penup()
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
        elif c == '.':
            increment_color(0)
        elif c == ',':
            increment_color(0, True)
        elif c == ':':
            increment_color(1)
        elif c == ';':
            increment_color(1, True)
        elif c == '!':
            increment_color(2)
        elif c == '?':
            increment_color(2, True)
        # Other:
        elif c == '{':
            if fill_color:
                t.begin_fill()
        elif c == '}':
            if fill_color:
                t.end_fill()
            gif_handler()
        elif c == '@':
            if fill_color:
                t.dot(None, fill_color)
            gif_handler()
        elif c == '`':
            swap_cases = not swap_cases
        elif c == '"':
            orient(t, position, None)
        elif c == "'":
            orient(t, None, heading)
        elif c == '$':
            stack.clear()
            t.clear()
        elif c == '[':
            stack.append(State((t.xcor(), t.ycor()), t.heading(), angle, length, thickness,
                               pen_color, fill_color, swap_signs, swap_cases, modify_fill))
        elif c == ']':
            if stack:
                state = stack.pop()
                orient(t, state.position, state.heading)
                angle, length = state.angle, state.length
                swap_signs, swap_cases, modify_fill = state.swap_signs, state.swap_cases, state.modify_fill
                pen_color, fill_color = state.pen_color, state.fill_color
        elif c == '\\':
            break

    if gif:
        if draws % draws_per_frame != 0:
            save_frame()  # Save frame of final changes unless nothing has changed.
        message(f'Prepped {len(gif_data)} gif frames of {frames_attempted} attempted for {draws + 1} draws.')

    return gif_data


if __name__ == '__main__':
    init((600, 600), ghostscript='')
    draw('A', 'A 0B-2A-3B B 4A+5B+6A', 60, 8, 5, 2, heading=150, position=(200, 00), red_increment=-2,
         color=None,
         png='', max_frames=500, draws_per_frame=20, alternate=False, thickness_increment=2,
         padding=None,  speed=10, asap=False, reverse=False, tmpdir='', show_turtle=False,
         turtle_shape='turtle', duration=30, output_scale=2)
    wait()
