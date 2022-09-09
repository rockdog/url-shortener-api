import pytest

from shortener import logic
from shortener import util


def test_create_url(session, target_url):
    key = util.generate_random_key(5)
    secret_key = util.generate_random_key(12)

    url = logic.url.create_url(
        session,
        url=target_url,
        key=key,
        secret_key=secret_key,
    )

    assert url.id is not None
    assert url.is_active
    assert url.clicks == 0
    assert url.key == key
    assert url.secret_key == secret_key
    assert url.created_at is not None
    assert url.updated_at is not None


def test_get_urls(session, url):
    assert len(logic.url.get_urls(session)) > 0


def test_get_url_by_key(session, url):
    assert logic.url.get_url_by(session, key=url.key) == url


def test_get_url_by_secret_key(session, url):
    assert logic.url.get_url_by(session, secret_key=url.secret_key) == url


def test_get_url_by_multiple_args(session):
    with pytest.raises(ValueError):
        logic.url.get_url_by(session, key="foo", secret_key="bar")
