
# def koch1(level=4, angle=90):
#     start = 'F'
#     rules = {'F': 'F+F-F-F+F'}
#     lsystem(start, rules, level, angle)


# def koch2(level=4):
#     start = 'L'
#     rules = {'L': 'L+L--L+L'}
#     lsystem(start, rules, level, 60, 1)


# def koch3(level=4):
#     start = 'A--B--C--'
#     rules = {
#         'A': 'A+A--A+A',
#         'B': 'B+B--B+B',
#         'C': 'C+C--C+C',
#     }
#     lsystem(start, rules, level, 60, 1)


# def sierpinski(level=4):
#     s = 'F-G-G'
#     r = 'F F-G+F+G-F G GG'
#     lsystem(s, r, level, -120, 15)


# def sierpinski2(level=6):
#     s = 'A'
#     r = 'A B-A-B B A+B+A'
#     lsystem(s, r, level, 60, 3)


# def cantor(levels=7):
#     s = 'A'
#     r = 'A AbA b bbb'
#     for i in range(levels):
#         lsystem(s, r, i, 0, 3**(levels - i - 1), color='white', y=10*i)


# def dragon(level=12):
#     s = 'F'
#     r = 'F F+G G F-G'
#     lsystem(s, r, level, 90, 8, (255, 190, 90))
