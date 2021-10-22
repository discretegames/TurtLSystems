#  type: ignore
"""Turns function docstring arguments list into markdown table."""

import re
import pyperclip
pattern = r'- `(.*?)=(.*?)` \((.*?)\):(.*?)(?=^        -)'

args = """
        - `window_size=(0.75, 0.75)` (Tuple[int | float, int | float]):
            The size of the window. Use integers for pixel dimensions. Use floats for a percentage of the screen size.
        - `window_title="TurtLSystems"` (str):
            The title of the window.
        - `background_color=(0, 0, 0)` (Tuple[int, int, int]):
            The background color of the window. A 0-255 rgb tuple. May be changed later by draw calls.
        - `background_image=None` (str | None):
            The file path to a background image for the window.
        - `window_position=None` (Tuple[int | None, int | None] | None):
            The top and left screen coordinates of the window, or None for centered.
        - `canvas_size=None` (Tuple[int | None, int | None] | None):
            The size of the drawing canvas when an area larger than the window size is desired.
        - `ghostscript=None` (str | None):
            The path to or command name of ghostscript.
            When None, an educated guess of the path is made on Windows and 'gs' is used on Mac/Linux.
            Ghostscript is the image conversion tool required for png and gif output:
            https://ghostscript.com/releases/gsdnld.html
        - `logo_mode=False` (bool):
            Whether the turtle graphics coordinates mode is 'standard' or 'logo'. Defaults to standard.
            In standard mode an angle of 0 points rightward and positive angles go counterclockwise.
            In logo mode an angle of 0 points upward and positive angles go clockwise.
        - `delay=None` (int | None):
            The turtle graphics animation delay in milliseconds. None for default value.
        - `silent=False` (bool):
            Whether to silence all messages and warnings produced by TurtLSystems.
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
    table += f'| {name}<br>`{default}` | {desc}<br>`{type_}`\n'

print(table)
pyperclip.copy(table)
