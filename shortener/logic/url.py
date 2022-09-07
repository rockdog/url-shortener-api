from typing import List

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
