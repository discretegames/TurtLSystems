"""Use `py test.py` for a quick way to run pytest tox and coverage."""

import os
from subprocess import run

print('Running Coverage...')
run('venv/Scripts/python -m coverage run -m pytest', check=False)

try:
    os.remove('coverage.svg')
except FileNotFoundError:
    pass
run('venv/Scripts/python -m coverage_badge -o coverage.svg', check=False)

try:
    os.remove('coverage.txt')
except FileNotFoundError:
    pass
run('venv\\Scripts\\python -m coverage report > coverage.txt', shell=True, check=False)

run('venv/Scripts/python -m coverage report', check=False)
run('venv/Scripts/python -m coverage html', check=False)
run('cmd /c start htmlcov/index.html', check=False)
print('COVERAGE DONE')


print('Running Tox...')
run('venv/Scripts/python -m tox', check=False)
print('TOX DONE')
