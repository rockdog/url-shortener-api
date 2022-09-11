import secrets
import string

from shortener import schemas
from shortener.config import base_url
from shortener.routes import manage_url

MAX_LENGTH = 256


def generate_random_key(length: int = 5) -> str:
    assert length <= MAX_LENGTH, f"limit must be smaller or equal than {MAX_LENGTH}"
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def to_url_info(url: schemas.URL) -> schemas.URLInfo:
    url.url = str(base_url().replace(path=url.key))
    url.admin_url = str(base_url().replace(path=manage_url.format(secret_key=url.secret_key)))
    return url
