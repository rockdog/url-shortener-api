import validators
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

from shortener import logic
from shortener import models
from shortener import schemas
from shortener.database import engine
from shortener.database import get_session
from shortener.util import generate_random_key

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
def read_root():
    return {"detail": "Welcome to the URL shortener API"}


@app.get("/urls", response_model=schemas.URLInfoList)
def get_urls(
    session: Session = Depends(get_session),
):
    return {
        "urls": logic.url.get_urls(session),
    }


@app.post("/url", response_model=schemas.URLInfo)
def create_url(
    url: schemas.URLBase,
    session: Session = Depends(get_session),
):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    url = logic.url.create_url(
        session=session,
        url=url.target_url,
        key=generate_random_key(5),
        secret_key=generate_random_key(8),
    )

    return url
