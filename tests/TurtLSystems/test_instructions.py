"""File to test L-system character instructions."""

import string
import random
from TurtLSystems import draw


def test_letters() -> None:
    """Testing A-Z and a-z."""
    for c in string.ascii_letters:
        length = random.randint(1, 100)
        _, t = draw(c, '', length=length)
        assert t.xcor() == length
        if c.isupper():
            assert t.isdown()
        else:
            assert not t.isdown()


def test_numbers() -> None:
    """Testing 0-9."""
    assert draw('0', '')[1].pencolor() == (255, 255, 255)
    assert draw('1', '')[1].pencolor() == (128, 128, 128)
    assert draw('2', '')[1].pencolor() == (255, 0, 0)
    assert draw('3', '')[1].pencolor() == (255, 128, 0)
    assert draw('4', '')[1].pencolor() == (255, 255, 0)
    assert draw('5', '')[1].pencolor() == (0, 255, 0)
    assert draw('6', '')[1].pencolor() == (0, 255, 255)
    assert draw('7', '')[1].pencolor() == (0, 0, 255)
    assert draw('8', '')[1].pencolor() == (128, 0, 255)
    assert draw('9', '')[1].pencolor() == (255, 0, 255)


def test_plusminus() -> None:
    """Testing + -."""
    assert draw('ff+f', '', angle=90, length=10)[1].pos() == (20, 10)
    assert draw('ff-f', '', angle=90, length=10)[1].pos() == (20, -10)
    assert draw('f+-f', '', angle=45, length=10)[1].pos() == (20, 0)


# TODO test the rest


if __name__ == '__main__':
    test_plusminus()
