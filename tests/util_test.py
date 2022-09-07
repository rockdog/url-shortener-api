import pytest

from shortener import util


def test_generate_random_key():
    assert len(util.generate_random_key(20)) == 20


def test_generate_random_key_too_long():
    with pytest.raises(AssertionError):
        util.generate_random_key(util.MAX_LENGTH + 1)
