import validators
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from shortener import exceptions as exc
from shortener import logic
from shortener import models
from shortener import routes
from shortener import schemas
from shortener.database import engine
from shortener.database import get_session
from shortener.util import generate_random_key
from shortener.util import to_url_info


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get(routes.home)
def read_root():
    return {"detail": "Welcome to the URL shortener API"}


@app.get(routes.urls, response_model=schemas.URLInfoList)
def get_urls(
    session: Session = Depends(get_session),
):
    return {
        "urls": [to_url_info(url) for url in logic.url.get_urls(session)],
    }


@app.post(routes.urls, response_model=schemas.URLInfo)
def create_url(
    url: schemas.URLBase,
    session: Session = Depends(get_session),
):
    if not validators.url(url.target_url):
        exc.raise_bad_request(message="Your provided URL is not valid")

    url = logic.url.create_url(
        session=session,
        url=url.target_url,
        key=generate_random_key(5),
        secret_key=generate_random_key(8),
    )

    return to_url_info(url)


@app.get(routes.get_url)
def redirect_to_target_url(
    url_key: str,
    request: Request,
    session: Session = Depends(get_session),
):
    if url := logic.url.get_url_by(session, key=url_key):
        logic.url.incr_url_clicks(session, url)
        return RedirectResponse(url.target_url)
    else:
        exc.raise_not_found(request)


@app.get(routes.manage_url, response_model=schemas.URLInfo)
def manage_url(
    secret_key: str,
    request: Request,
    session: Session = Depends(get_session),
):
    if url := logic.url.get_url_by(session, secret_key=secret_key):
        return to_url_info(url)
    else:
        exc.raise_not_found(request)


@app.delete(routes.manage_url)
def delete_url(secret_key: str, request: Request, session: Session = Depends(get_session)):
    if url := logic.url.deactivate_url_by(session, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{url.target_url}'"
        return {"detail": message}
    else:
        exc.raise_not_found(request)
