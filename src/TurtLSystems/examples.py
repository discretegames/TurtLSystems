"""TurtLSystems examples (https://pypi.org/project/turtlsystems)."""

from turtlsystems import draw, wait

try:
    # draw('A', 'A B-A-B B A+B+A.', 5, 60, 7, 2,
    #      color=(200, 220, 255),
    #      fill_color=(255, 255, 255),
    #      background_color=(36, 8, 107),
    #      red_increment=-2,
    #      max_frames=None,
    #      frame_every=3,
    #      duration=30,
    #      heading=60,
    #      #  gif='example.gif',
    #      asap=True)

    draw('X', 'X 0F-[[X]+X]-1F[+FX]-X F FF',
         5, angle=10, length=5, thickness=2, heading=90, position=(0, -200),
         color=(5, 190, 10),
         scale=1.2,
         fill_color=(2, 222, 30),
         background_color=(120, 30, 9),
         asap=True,
         png='fern')
    wait()
except:  # noqa
    pass
