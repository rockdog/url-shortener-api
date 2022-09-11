import pytest

from shortener import util


def test_generate_random_key():
    assert len(util.generate_random_key(20)) == 20


def test_generate_random_key_too_long():
    with pytest.raises(AssertionError):
        util.generate_random_key(util.MAX_LENGTH + 1)


def test_to_url_info(url):
    url_info = util.to_url_info(url)
    assert url_info.url is not None
    assert url_info.admin_url is not None
