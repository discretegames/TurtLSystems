"""The TurtLSystems Python package (https://pypi.org/project/TurtLSystems) is a tool and educational
code toy for generating images and animations of Lindenmayer system (L-system) patterns via turtle graphics."""
from TurtLSystems.core import draw
from TurtLSystems.core import Exit
from TurtLSystems.core import init
from TurtLSystems.core import lsystem
from TurtLSystems.core import wait

__all__ = ['init', 'draw', 'wait', 'lsystem', 'Exit']
