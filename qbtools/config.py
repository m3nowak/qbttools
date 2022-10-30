import datetime as dt
import typing as ty

import pydantic as pyd


class _Base(pyd.BaseModel):
    class Config:
        json_encoders = {
            # custom output conversion for datetime
            dt.date: lambda v: v.strftime('%Y-%m-%d')
        }


class QbtAccessConfig(_Base):
    host: str
    port: int
    username: str
    password: str


class FeedRule(_Base):
    category: ty.Optional[str]
    date_limit: ty.Optional[dt.date]
    save_path: ty.Optional[str]
    phrase: str


class FeedConfig(_Base):
    url: str
    rules: ty.List[FeedRule]


class Config(_Base):
    qbt_access: QbtAccessConfig
    expire_default: int
    feeds: ty.List[FeedConfig]


def produce_default_config() -> Config:
    return Config(
        expire_default=30,
        qbt_access=QbtAccessConfig(
            host='localhost',
            port=8080,
            username='user',
            password='pass'
        ),
        feeds=[FeedConfig(
            url='http://example.com/rss',
            rules=[
                FeedRule(
                    date_limit=dt.date(2020, 1, 1),
                    phrase='linux distribution',
                    category='linux',
                    save_path='/some/dir/idk'
                )
            ]
        )]
    )
