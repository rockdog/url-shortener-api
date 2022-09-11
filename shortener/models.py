import datetime

import pytz
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from shortener.database import Base


def utc_now():
    return datetime.datetime.now(tz=pytz.timezone("UTC"))


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False, unique=True, index=True)
    secret_key = Column(String, nullable=False, unique=True, index=True)
    target_url = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
