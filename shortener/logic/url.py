from typing import List
from typing import Optional

from shortener import models


def create_url(session, url, key: str, secret_key: str) -> models.URL:
    _url = models.URL(
        target_url=url,
        key=key,
        secret_key=secret_key,
    )
    session.add(_url)
    session.commit()
    session.refresh(_url)

    # TODO(remove this)
    _url.url = _url.key
    _url.admin_url = _url.secret_key

    return _url


def get_url_by(session, key: Optional[str] = None, secret_key: Optional[str] = None) -> Optional[models.URL]:
    if len([arg for arg in [key, secret_key] if arg is not None]) != 1:
        raise ValueError("must pass one of 'key' or 'secret_key")

    query = session.query(models.URL)

    if key:
        query = query.filter(models.URL.key == key, models.URL.is_active)
    elif secret_key:
        query = query.filter(models.URL.secret_key == secret_key, models.URL.is_active)

    return query.first()


def get_urls(session) -> List[models.URL]:
    # TODO(pagination, order)
    result = []
    _urls = session.query(models.URL).all()
    for url in _urls:
        # TODO(remove this)
        url.url = url.key
        url.admin_url = url.secret_key
        result.append(url)
    return result
