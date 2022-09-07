import datetime
from typing import List

from pydantic import BaseModel


class URLBase(BaseModel):
    target_url: str


class URL(URLBase):
    is_active: bool
    clicks: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class URLInfo(URL):
    url: str
    admin_url: str


class URLInfoList(BaseModel):
    urls: List[URLInfo]
