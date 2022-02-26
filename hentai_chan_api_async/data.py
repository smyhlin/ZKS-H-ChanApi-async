from dataclasses import dataclass
from .parsers.content import MangaContent


@dataclass
class Manga:
    id: str = None
    title: str = None
    poster: str = None
    series: str = None
    author: str = None
    original_url: str = None
    translator: str = None
    content: MangaContent = None
    tags: list = None
    date: str = None
