"""The turtlsystems Python package (https://pypi.org/project/turtlsystems) is a tool and educational
code toy for generating images and animations of Lindenmayer system (L-system) patterns via turtle graphics."""

from turtlsystems.core import init
from turtlsystems.core import draw
from turtlsystems.core import wait
from turtlsystems.core import lsystem
__all__ = ['init', 'draw', 'wait', 'lsystem']
