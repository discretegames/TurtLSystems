"""An implementation of Lindenmayer systems in Python with turtle graphics."""

from typing import List
import turtle
from defaults import Default

IS_SETUP = False
IS_FINISHED = False


def get(value, default):
    return default if value is None else value


def finish():
    global IS_FINISHED
    if not IS_FINISHED:
        IS_FINISHED = True
        turtle.done()


def setup(title="TurtLSystems", window_size=(0.75, 0.75), background_color=(0, 0, 0), background_image=None,
          canvas_size=(None, None), window_position=(None, None), delay=0, mode='standard'):
    turtle.colormode(255)
    turtle.title(str(get(title, Default.title)))
    turtle.mode(get(mode, Default.mode))
    turtle.delay(get(delay, Default.delay))
    window_w, window_h = get(window_size, Default.window_size)
    window_x, window_y = get(window_position, Default.window_position)
    turtle.setup(window_w, window_h, window_x, window_y)
    canvas_w, canvas_h = get(canvas_size, Default.canvas_size)
    turtle.screensize(canvas_w, canvas_h)
    turtle.bgcolor(get(background_color, Default.background_color))
    turtle.bgpic(get(background_image, Default.background_image))
    global IS_SETUP
    IS_SETUP = True
# todo draws_per_frame, png_out/pad, gif_out/pad


def parse_rules(rules):
    if isinstance(rules, str):
        r = rules.split()
        rules = {inp: out for inp, out in zip(r[::2], r[1::2])}
    return rules


def make_colors(color, fill_color, colors):
    colors = list(map(tuple, colors))
    colors.extend(Default.colors[len(colors):])
    if color is not None:
        colors[0] = tuple(color)
    if fill_color is not None:
        colors[1] = tuple(fill_color)
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


def expand_lsystem(start, rules, n):
    for _ in range(n):
        start = ''.join(rules.get(c, c) for c in start)
    return start


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


def run(t: turtle.Turtle, string, *, colors, full_circle, angle, length, thickness, angle_increment,
        length_increment, length_scalar, thickness_increment, color_increments):
    initial_angle, initial_length = angle, length
    swap_signs, change_fill = False, False
    pen_color, fill_color = colors[0], colors[1]
    t.pencolor(pen_color)
    t.fillcolor(fill_color)
    stack: List[State] = []

    def set_color(color):
        nonlocal pen_color, fill_color, change_fill
        if change_fill:
            change_fill = False
            fill_color = color
            t.fillcolor(fill_color)
        else:
            pen_color = color
            t.pencolor(pen_color)

    def increment_color(channel, decrement=False):
        color = list(fill_color if change_fill else pen_color)
        amount = (1 if decrement else -1) * color_increments[channel]
        color[channel] = max(0, min(color[channel] + amount, 255))
        set_color(tuple(color))

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
                swap_signs, change_fill = s.swap_signs, s.change_fill
                pen_color, fill_color = s.pen_color, s.fill_color
        elif c == '$':
            break


def draw(start='F', rules='F F+F-F-F+F', n=4, angle=90, length=10, thickness=1, color=(255, 0, 0),
         fill_color=(255, 128, 0), background_color=(0, 0, 0), *, colors=None,
         angle_increment=15, length_increment=5, length_scalar=2, thickness_increment=1,
         red_increment=4, green_increment=4, blue_increment=4, position=(0, 0), heading=0,
         speed=0, asap=False, show_turtle=False, turtle_shape='classic', full_circle=360.0, finish=True):
    if not IS_SETUP:
        setup()

    turtle.colormode(255)
    turtle.bgcolor(get(background_color, Default.background_color))
    asap = get(asap, Default.asap)
    if asap:
        saved_tracer, saved_delay = turtle.tracer(), turtle.delay()
        turtle.tracer(0, 0)

    t = turtle.Turtle()
    full_circle = get(full_circle, Default.full_circle)
    t.degrees(full_circle)
    t.speed(get(speed, Default.speed))
    t.shape(get(turtle_shape, Default.turtle_shape))
    if get(show_turtle, Default.show_turtle):
        t.showturtle()
    else:
        t.hideturtle()
    orient(t, get(position, Default.position), get(heading, Default.heading))

    rules = parse_rules(get(rules, Default.rules))
    string = expand_lsystem(get(start, Default.start), rules, get(n, Default.n))
    colors = make_colors(get(color, Default.color), get(fill_color, Default.fill_color), get(colors, Default.colors))

    run(t, string, colors=colors, full_circle=full_circle,
        angle=get(angle, Default.angle),
        length=get(length, Default.length),
        thickness=get(thickness, Default.thickness),
        angle_increment=get(angle_increment, Default.angle_increment),
        length_increment=get(length_increment, Default.length_increment),
        length_scalar=get(length_scalar, Default.length_scalar),
        thickness_increment=get(thickness_increment, Default.thickness_increment),
        color_increments=(get(red_increment, Default.red_increment),
                          get(green_increment, Default.green_increment),
                          get(blue_increment, Default.blue_increment)))

    if asap:
        turtle.tracer(saved_tracer, saved_delay)
        turtle.update()
    if get(finish, Default.finish):
        finish()

    return string, tuple(t.position()), t.heading()
