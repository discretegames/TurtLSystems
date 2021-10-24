# type: ignore
"""Turns function docstring arguments list into markdown table."""

import re
import pyperclip

pattern = r'- `(.*?)=(.*?)` \((.*?)\):(.*?)(?=\Z|^        -)'

args = pyperclip.paste()


def clean(part):
    """Cleans part of arg."""
    part = part.strip().replace('|', '\\|')
    part = re.sub('\r?\n', ' ', part)
    return re.sub(' +', ' ', part)


table = """
| Arg Name<br>`Default Value` | Description<br>`Type` |
| --------------------------- | --------------------- |
"""
args = [tuple(map(clean, arg)) for arg in re.findall(pattern, args, re.DOTALL | re.MULTILINE)]
for name, default, type_, desc in args:
    # table += f'| `{name}` | `{default}` | `{type_}` | {desc}\n'
    table += f'| {name}<br>`{default}` | {desc}<br>`{type_}`\n'

table = table.strip('\n')

print(table)
pyperclip.copy(table)
