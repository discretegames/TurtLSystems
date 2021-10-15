"""An implementation of Lindenmayer systems in Python with turtle graphics."""

import turtle


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
# todo starting example with just draw()? sure, so defaults for start, rule, import from examples
# todo draws_per_frame, png_out/pad, gif_out/pad


def expand_lsystem(start, rules, level):
    for _ in range(level):
        start = ''.join(rules.get(c, c) for c in start)
    return start


def parse_rules(rules):
    if isinstance(rules, str):
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
        if turtle.colormode() == 1.0:
            defaults = [(r/255, g/255, b/255) for r, g, b in defaults]
        colors = colors + defaults[len(colors):]
        if color is not None:
            colors[0] = color
        if fill_color is not None:
            colors[1] = fill_color
    return colors


def run(t, string, colors, angle, length, thickness, angle_increment, length_increment, length_scalar,
        thickness_increment, red_increment, green_increment, blue_increment):
    pass


# todo? get-ify all these?
def draw(start, rules, level=4, angle=90, length=20, thickness=1, color=(255, 255, 255),
         fill_color=(128, 128, 128), background_color=(0, 0, 0), *, colors=None,
         angle_increment=15, length_increment=5, length_scalar=2, thickness_increment=1,
         red_increment=8, green_increment=8, blue_increment=8, position=(0, 0), heading=0,
         instant=False, speed=10, show_turtle=False, turtle_shape="classic", full_circle=360.0):

    string = expand_lsystem(start, parse_rules(rules), level)
    colors = make_color_list(colors, fill_color, colors)

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
    t.pencolor(colors[0])
    t.fillcolor(colors[1])

    t.penup()
    t.speed(0)
    t.setposition(position)
    t.setheading(heading)
    t.speed(speed)
    t.pendown()

    run(t, string, colors, angle, length, thickness, angle_increment, length_increment,
        length_scalar, thickness_increment, red_increment, green_increment, blue_increment)

    if instant:
        turtle.tracer(saved_tracer, saved_delay)
    return tuple(t.position()), t.heading()


def show():
    turtle.done()
    turtle.update()


setup(background_image='bgpic.png', )
print(draw("", ""))
show()
