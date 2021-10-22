#  type: ignore
"""Turns function docstring arguments list into markdown table."""

import re
import pyperclip
pattern = r'- `(.*?)=(.*?)` \((.*?)\):(.*?)(?=^        -)'

args = """
        - `start='F+G+G'` (str):
            The initial string or axiom of the L-system. Level 0.
        - `rules='F F+G-F-G+F G GG'` (Dict[str, str] | str):
            Dictionary that maps characters to what they are replaced with in the L-system expansion step.
            May also be a string where whitespace separated pairs of substrings correspond to the character and its
            replacement. For example `{'A': 'AB', 'B': 'B+A'}` and `'A AB B B+A'` represent the same rules.
        - `level=4` (int):
            The number of L-system expansion steps to take, i.e. how many times to apply `rules` to `start`.
        - `angle=120` (float):
            The angle to turn by on `+` or `-`. In degrees by default but the `circle` arg can change that.
        - `length=20` (float):
            The distance in pixels to move forward by on letters. The length step.
        - `thickness=1` (float):
            The line width in pixels. May be any non-negative number.
        - `color=(255, 255, 255)` (Tuple[int, int, int] | None):
            The line color. A 0-255 rgb tuple or None to hide all lines. Reselected on `0`.
        - `fill_color=(128, 128, 128)` (Tuple[int, int, int] | None):
            The fill color for `{}` polygons, `@` dots, and turtle shapes. A 0-255 rgb tuple or None to hide all fills.
            Reselected on `1`.
        - `background_color=None` (Tuple[int, int, int] | None):
            The background color of the window. A 0-255 rgb tuple or None to leave unchanged.
        - `asap=False` (bool):
            When True the draw will happen as fast as possible, ignoring `speed` arg and the `delay` arg of `init`.
"""


def clean(part):
    """Cleans part of arg."""
    return part.strip().replace('|', '\\|').replace('\n', ' ')


table = """| Name | Default | Type | Description |
| ---- | ------- | ---- | ----------- |
"""
table = """
| Name<br>Default<br>Type | Description |
| ----------------------- | ----------- |
"""
args = [tuple(map(clean, arg)) for arg in re.findall(pattern, args, re.DOTALL | re.MULTILINE)]
for name, default, type_, desc in args:
    # table += f'| `{name}` | `{default}` | `{type_}` | {desc}\n'
    table += f'| `{name}`<br>`{default}`<br>`{type_}` | {desc}\n'

print(table)
pyperclip.copy(table)
