from turtle import heading, position, showturtle


class Default:
    title = "TurtLSystems"
    window_size = 0.75, 0.75
    window_position = None, None
    canvas_size = None, None
    background_color = 0, 0, 0
    background_image = None
    delay = 0
    mode = 'standard'
    start = 'F'
    rules = 'F F+F-F-F+F'
    n = 4
    angle = 90
    length = 10
    thickness = 1
    color = 255, 0, 0
    fill_color = 255, 128, 0
    colors = None
    colors_list = [
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
    angle_increment = 15
    length_increment = 5
    length_scalar = 2
    thickness_increment = 1
    red_increment = 4
    green_increment = 4
    blue_increment = 4
    position = 0, 0
    heading = 0
    speed = 0
    asap = False
    show_turtle = False
    turtle_shape = 'classic'
    full_circle = 360.0
    last = True
