import asyncio

from bs4 import BeautifulSoup

from .http import Http
from .parsers import page
from .data import Manga
from .parsers.content import MangaContent


class HentaiChan:
    _host = 'https://hentaichan.live'
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/97.0.4692.71 Safari/537.36',
    }

    def __init__(self, proxies: dict = None):
        self._proxy = proxies

    async def __bs_request(self, url: str, params: dict = None) -> BeautifulSoup:
        async with Http(headers=self._headers) as http:
            html = await http.get(url, params=params)
        return BeautifulSoup(html, 'html.parser')

    async def get_new(self, page_num: int = 1, count: int = 20) -> list[Manga]:
        """
        Метод возвращает count эл-тов (если возможно)
        новой манги, на странице номер page_num

        :param page_num: номер страницы.
        :param count: кол-во эл-тов страницы (максимум 20 на страницу)
        :return:
        """
        assert page_num >= 1, ValueError("Значение page_num не может быть меньше 1")
        assert count <= 20, ValueError("Значение count не может быть больше 20")

        offset = page_num * 20 - 20
        url = self._host + '/manga/new'
        return await self.__get_manga_list(url, count, offset)

    async def search(self, query: str = None, tag: str = None, page_num: int = 1, count: int = 20) -> list[Manga]:
        """
        Метод используется для осуществления поиска манги

        Доступен поиск как по ключевым фразам (query), так и по тегам (tag)

        :param page_num:
        :param count:
        :param query:
        :param tag:
        :return:
        """
        assert page_num >= 1, ValueError("Значение page_num не может быть меньше 1")
        assert count <= 20, ValueError("Значение count не может быть больше 20")

        offset = page_num * 20 - 20
        if tag:
            return await self.__get_manga_list(f'{self._host}/tags/{tag}', count=count, offset=offset)
        elif query:
            params = {'do': 'search', 'subaction': 'search', 'story': query}
            return await self.__get_manga_list(f'{self._host}/', count=count, offset=offset, params=params)
        elif tag and query:
            raise ValueError('Метод search получил сразу 2 аргумента для поиска, допустим только 1')
        else:
            raise ValueError('Метод search не получил аргументов для поиска')

    async def tags(self) -> list[str]:
        """
        Метод возвращает список всех tags
        доступных на сайте

        :return:
        """
        url = f'{self._host}/tags/'
        soup_content = await self.__bs_request(url)
        return page.parse_tags(soup_content)

    async def random(self, count=1) -> list[Manga]:
        """
        Метод возвращает рандомные manga в формате list[manga]
        Параметр count регулирует кол-во выданной манги за раз,
        причем count варьируется от 1 до 20.

        :param count: [1; 20]
        :return:
        """
        url = f'{self._host}/manga/random'
        return await self.__get_manga_list(url, count)

    async def manga(self, manga_id: str) -> Manga:
        """
        Метод возвращает объект Manga

        :param manga_id:
        :return:
        """
        url = f'{self._host}/manga/{manga_id}.html'
        content = await self.__bs_request(url)

        m = page.parse_manga(bs_content=content, manga_id=manga_id, host=self._host)
        m.content = MangaContent(self.__bs_request, manga=m)
        return m

    async def __get_manga_list(self, url: str, count: int, offset: int = 20, params: dict = {}) -> list[Manga]:
        """
        Вспомогательный метод, используется для парсинга манги из поисковой выдачи

        :param url:
        :param offset:
        :param params: params для url
        :return:
        """
        soup_content = await self.__bs_request(url, params={**params, 'offset': offset})
        manga_ids = page.parse_manga_ids(bs_content=soup_content, count=count, host=self._host)

        manga_list = await asyncio.gather(*(self.manga(manga_id) for manga_id in manga_ids))
        return manga_list
