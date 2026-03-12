from urllib.parse import urlparse
from abc import ABC, abstractmethod
from typing import Any
import re


class EmbededVideoHandler(ABC):
    def __init__(self, url):
        url_data = urlparse(url)
        self.url = url
        self.scheme = url_data.scheme
        self.netloc = url_data.netloc
        self.path = url_data.path
        self.query = url_data.query

    @abstractmethod
    def get_embed(self) -> Any:
        pass


class YouTubeHandler(EmbededVideoHandler):
    def get_embed(self) -> Any:
        print(self.netloc)
        if not self.netloc.startswith('www.'):
            self.netloc = f'www.{self.netloc}'
        if 'youtu.be' in self.netloc:
            self.netloc = f'www.youtube.com'
        if self.query:
            return f'//{self.netloc}/embed/{self.query.replace("v=","").replace(".","")}'
        else:
            return f'//{self.netloc}/embed/{self.path.replace("/","").replace(".","")}'


class SpotifyHandler(EmbededVideoHandler):
    def get_embed(self) -> Any:
        return f'//{self.netloc}/embed/{self.path}/{self.query}'


class DailymotionHandler(EmbededVideoHandler):
    def get_embed(self) -> Any:
        return f'//{self.netloc}/embed{self.path}'


class VimeoHandler(EmbededVideoHandler):
    def get_embed(self) -> Any:
        return f'//player.{self.netloc}/video{self.path}'


class TwitchHandler(EmbededVideoHandler):
    def get_embed(self) -> Any:
        print(vars(self))
        return f'//player.{self.netloc.replace('www.','')}/?video={self.path.replace('/videos/','')}'


class BandCampHandler(EmbededVideoHandler):
    def get_embed(self) -> Any:
        return ''

class WebsiteHandler(EmbededVideoHandler):
    def get_embed(self) -> Any:
        return self.url

HANDLERS = {
    'youtube.com': YouTubeHandler,
    'youtu.be': YouTubeHandler,
    'dailymotion.com': DailymotionHandler,
    'spotify.com': SpotifyHandler,
    'vimeo.com': VimeoHandler,
    'bandcamp.com': BandCampHandler
}


def get_handler(url: str) -> EmbededVideoHandler:
    domain = urlparse(url).netloc.lower().replace('www.', '')
    handler_class = HANDLERS.get(domain)
    if not handler_class:
        for handler_key in HANDLERS.keys():
            if handler_key in domain:
                handler_class = HANDLERS[handler_key]
    if handler_class:
        return handler_class(url)
    else:
        return WebsiteHandler(url)


def extract_urls(text: str) -> list[str]:
    url_pattern = re.compile(
        r'(?:https?://|www\.)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        re.IGNORECASE
    )
    urls = []
    for match in url_pattern.finditer(text):
        parsed = urlparse(match.group())
        urls.append(parsed.geturl()) if parsed.scheme else urls.append(f'https://{parsed.geturl()}')
    return urls


def extract_embed_sources(content):
    urls = extract_urls(content)
    for url in urls:
        handler = get_handler(url)
        if handler:
            yield handler.get_embed()
    return None
