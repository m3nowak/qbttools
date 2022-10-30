import datetime as dt
import typing as ty

import qbittorrentapi as qbtapi

from qbtools.config import QbtAccessConfig


class NotSetUpException(Exception):
    pass


class QbtSvc():
    _client: qbtapi.Client
    _config: QbtAccessConfig
    version: str
    is_set_up: bool

    def __init__(self, config: QbtAccessConfig):
        self._config = config
        self.is_set_up = False

    def setup(self):
        self._client = qbtapi.Client(
            self._config.host,
            self._config.port,
            self._config.username,
            self._config.password)
        self.version = self._client.app.version
        self.is_set_up = True

    def _assure_setup(self):
        if not self.is_set_up:
            raise NotSetUpException()

    def _list_with_category(self, category: str) -> ty.Iterable[qbtapi.torrents.TorrentDictionary]:
        '''Fix for bad internal typing'''
        return self._client.torrents_info(category=category)

    def remove_category_from_old(self, category: str, limit: dt.datetime) -> int:
        self._assure_setup()
        counter = 0
        limit_ts = dt.datetime.timestamp(limit)
        for torrent in self._list_with_category(category):
            if torrent.added_on < limit_ts:
                self._client.torrents_set_category('', torrent.hash)
                counter += 1
        return counter

    def pause_category(self, category: str) -> int:
        self._assure_setup()
        counter = 0
        for torrent in self._list_with_category(category):
            self._client.torrents_pause(torrent.hash)
            counter += 1
        return counter
    
    def resume_category(self, category: str) -> int:
        self._assure_setup()
        counter = 0
        for torrent in self._list_with_category(category):
            self._client.torrents_resume(torrent.hash)
            counter += 1
        return counter
    
    

    def add_magnet(self, magnet_link: str, start: bool = True, category: ty.Optional[str] = None, save_path: ty.Optional[str] = None):
        self._assure_setup()
        if not category:
            category = ''
        self._client.torrents_add(
            magnet_link, download_path=save_path, category=category, is_paused=not start)
