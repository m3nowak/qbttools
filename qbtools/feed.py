import datetime as dt
import time
import typing as ty

import feedparser
import dateutil.parser as du_parser


class NotLoadedException(Exception):
    pass


class Feed:
    _feedparsed = feedparser.util.FeedParserDict
    url: str
    is_loaded: bool

    def __init__(self, url: str) -> None:
        self.url = url
        self.is_loaded = False

    def load(self):
        self._feedparsed = feedparser.parse(self.url)
        self.is_loaded = True

    def _assure_loaded(self):
        if not self.is_loaded:
            raise NotLoadedException()

    def filter_by_title(self, title_phrase: str, not_before: ty.Optional[dt.date]) -> ty.Iterable[feedparser.util.FeedParserDict]:
        self._assure_loaded()
        not_before_dt = None if not_before is None else dt.datetime(
            not_before.year, not_before.month, not_before.day, 0, 0, 0)
        title_phrase_upper = title_phrase.upper()
        for entry in self._feedparsed.entries:
            pub_par = du_parser.parse(entry.published).replace(tzinfo=None)
            if title_phrase_upper in entry.title.upper() and \
                    (not_before is None or pub_par > not_before_dt):
                yield entry
