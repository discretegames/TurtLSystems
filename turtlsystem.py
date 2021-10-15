"""An implementation of Lindenmayer systems in Python with turtle graphics."""

from typing import List

import turtle


WAS_SETUP = False

# todo have defaults up here as we can?


def get(value, default=None):
    return default if value is None else value


def setup(title="TurtLSystems", window_size=(0.75, 0.75), background_color=(0, 0, 0), background_image=None,
          canvas_size=(None, None), window_position=(None, None), delay=0, color_mode=255, mode="standard"):
    turtle.title(str(get(title, "TurtLSystems")))
    turtle.colormode(get(color_mode, 255))
    turtle.mode(get(mode, "standard"))
    turtle.delay(get(delay, 0))
    window_w, window_h = get(window_size, (0.75, 0.75))
    window_x, window_y = get(window_position, (None, None))
    turtle.setup(window_w, window_h, window_x, window_y)
    canvas_w, canvas_h = get(canvas_size, (None, None))
    turtle.screensize(canvas_w, canvas_h)
    turtle.bgcolor(get(background_color, (0, 0, 0)))
    turtle.bgpic(background_image)
    global WAS_SETUP
    WAS_SETUP = True
# todo starting example with just draw()? sure, so defaults for start, rule, import from examples
# todo draws_per_frame, png_out/pad, gif_out/pad


def expand_lsystem(start, rules, level):
    for _ in range(level):
        start = ''.join(rules.get(c, c) for c in start)
    return start


def parse_rules(rules):
    if rules is None:
        rules = {}
    elif isinstance(rules, str):
        r = rules.split()
        rules = {inp: out for inp, out in zip(r[::2], r[1::2])}
    return rules  # todo maybe warn here about invalid rules


def make_color_list(color, fill_color, colors):
    if colors is None:
        colors = []
    if len(colors) < 10:
        defaults = [
            (255, 0, 0),
            (255, 128, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 255, 255),
            (0, 0, 255),
            (128, 0, 255),
            (255, 0, 255),
            (128, 128, 128),
            (255, 255, 255)
        ]
        if turtle.colormode() == 1.0:  # TODO map colors to tuples
            defaults = [(r/255.0, g/255.0, b/255.0) for r, g, b in defaults]
        colors = colors + defaults[len(colors):]
        if color is not None:
            colors[0] = color
        if fill_color is not None:
            colors[1] = fill_color
    return colors


def orient(t: turtle.Turtle, position, heading):
    speed = t.speed()
    down = t.isdown()
    t.penup()
    t.speed(0)
    t.setposition(position)
    t.setheading(heading)
    t.speed(speed)
    if down:
        t.pendown()


class State:
    def __init__(self, position, heading, angle, length, thickness, pen_color, fill_color,
                 swap_signs, change_fill):
        self.position = tuple(position)
        self.heading = heading
        self.angle = angle
        self.length = length
        self.thickness = thickness
        self.pen_color = pen_color
        self.fill_color = fill_color
        self.swap_signs = swap_signs
        self.change_fill = change_fill


# todo remove colormode 1.0, only support 255, no names
# todo tuples for all colors? yeah, should do that YES
def run(t: turtle.Turtle, string, colors, angle, length, thickness, angle_increment,
        length_increment, length_scalar, thickness_increment, color_increments, full_circle):
    initial_angle, initial_length = angle, length
    swap_signs, change_fill = False, False
    pen_color, fill_color = list(colors[0]), list(colors[1])
    t.pencolor(pen_color)
    t.fillcolor(fill_color)
    stack: List[State] = []

    def set_color(color=None):
        nonlocal pen_color, fill_color, change_fill
        if change_fill:
            change_fill = False
            if color:
                fill_color = list(color)
            t.fillcolor(fill_color)
        else:
            if color:
                pen_color = list(color)
            t.pencolor(pen_color)

    def increment_color(channel, decrement=False):
        color = fill_color if change_fill else pen_color
        amount = (1 if decrement else -1) * color_increments[channel]
        color[channel] = max(0, min(color[channel] + amount, 255))
        set_color()

    for c in string:
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
        elif c == '>':
            angle += angle_increment
        elif c == '<':
            angle -= angle_increment
        # Thickness:
        elif c == '=':
            t.pensize(thickness)
        elif c == ')':
            t.pensize(max(1, thickness + thickness_increment))
        elif c == '(':
            t.pensize(max(1, thickness - thickness_increment))
        # Color:
        elif '0' <= c <= '9':
            set_color(c)
        elif c == '#':
            change_fill = True
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
            stack.append(State(t.position(), t.heading(), angle, length, thickness,
                         pen_color, fill_color, swap_signs, change_fill))
        elif c == ']':
            if stack:
                s = stack.pop()
                orient(t, s.position, s.heading)
                angle, length = s.angle, s.length
                pen_color, fill_color = s.pen_color, s.fill_color
                swap_signs, change_fill = s.swap_signs, s.change_fill
        elif c == '$':
            break


# todo? get-ify all these? probably, watch out for colors and rules
def draw(start="F", rules=None, level=4, angle=90, length=20, thickness=1, color=(255, 0, 0),
         fill_color=(255, 128, 0), background_color=(0, 0, 0), *, colors=None, last=True,
         angle_increment=15, length_increment=5, length_scalar=2, thickness_increment=1,
         red_increment=8, green_increment=8, blue_increment=8, position=(0, 0), heading=0,
         instant=False, speed=0, show_turtle=False, turtle_shape="classic", full_circle=360.0):
    if not WAS_SETUP:
        setup()

    string = expand_lsystem(start, parse_rules(rules), level)
    colors = make_color_list(color, fill_color, colors)

    turtle.bgcolor(background_color)
    if instant:
        saved_tracer, saved_delay = turtle.tracer(), turtle.delay()
        turtle.tracer(0, 0)

    t = turtle.Turtle()
    t.degrees(full_circle)
    t.shape(turtle_shape)
    if show_turtle:
        t.showturtle()
    else:
        t.hideturtle()
    orient(t, position, heading)
    run(t, string, colors, angle, length, thickness, angle_increment, length_increment, length_scalar,
        thickness_increment, (red_increment, green_increment, blue_increment), full_circle)

    if instant:
        turtle.tracer(saved_tracer, saved_delay)
        turtle.update()
    if last:
        turtle.done()

    return tuple(t.position()), t.heading()


def done():
    turtle.done()


# print(draw("F", {'F': 'F+F-F-F+F'}, angle=45, instant=True, last=False))
draw("FF4|FFF")
