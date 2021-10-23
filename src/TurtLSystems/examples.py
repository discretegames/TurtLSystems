"""TurtLSystems examples (https://pypi.org/project/TurtLSystems)."""

from TurtLSystems import init, draw, wait, Exit
try:
    init(...)
    draw(...)
    wait()
except Exit:
    pass

# from TurtLSystems import init, draw,
# draw('+A', 'A B-A-B B A+B+A,', 5, 60, 7, 2, (200, 220, 255), None, (36, 8, 107),
#      red_increment=2, gif='example.gif', max_frames=250, duration=30)
# # try:

# draw('X', 'X 0F-[[X]+X]-1F[+FX]-X F FF',
#      5, angle=10, length=5, thickness=2, heading=90, position=(0, -200),
#      color=(5, 190, 10),
#      scale=1.2,
#      fill_color=(2, 222, 30),
#      background_color=(120, 30, 9),
#      asap=True,
#      png='fern')
# wait()
# except:  # noqa # pylint: disable=bare-except
#     pass
