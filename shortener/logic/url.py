from typing import List
from typing import Optional

from sqlalchemy import desc

from shortener import models

DEFAULT_LIMIT = 100
DEFAULT_OFFSET = 0


def create_url(session, url, key: str, secret_key: str) -> models.URL:
    _url = models.URL(
        target_url=url,
        key=key,
        secret_key=secret_key,
    )
    session.add(_url)
    session.commit()
    session.refresh(_url)
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


def get_urls(session, limit: Optional[int] = None, offset: Optional[int] = None) -> List[models.URL]:
    if not limit:
        limit = DEFAULT_LIMIT
    if not offset:
        offset = DEFAULT_OFFSET
    return session.query(models.URL).order_by(desc(models.URL.created_at)).limit(limit).offset(0).all()


def deactivate_url_by(session, secret_key: str) -> Optional[models.URL]:
    if url := get_url_by(session, secret_key=secret_key):
        url.is_active = False
        session.commit()
        return url


def incr_url_clicks(session, url):
    url.clicks += 1
    session.commit()
    return url
