import asyncio
import re

from .data import Manga
from .content_parser import MangaContent
from bs4 import BeautifulSoup

from .http import Http


class HentaiChan:
    _host = 'https://hentaichan.live'
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/97.0.4692.71 Safari/537.36',
    }

    def __init__(self, proxies: dict = None):
        self._proxy = proxies

    async def __get_site_content(self, url: str, params: dict = None) -> BeautifulSoup:
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
        return await self.__get_search_content(url, offset, count)

    async def search(self, page_num: int = 1, count: int = 20, query: str = None, tag: str = None) -> list[Manga]:
        assert page_num >= 1, ValueError("Значение page_num не может быть меньше 1")
        assert count <= 20, ValueError("Значение count не может быть больше 20")

        offset = page_num * 20 - 20
        if tag:
            return await self.__get_search_content(f'{self._host}/tags/{tag}', count=count, offset=offset)
        elif query:
            params = {'do': 'search', 'subaction': 'search', 'story': query}
            return await self.__get_search_content(f'{self._host}/', count=count, offset=offset, params=params)
        elif tag and query:
            raise ValueError('Метод search получил сразу 2 аргумента для поиска, допустим только 1')
        else:
            raise ValueError('Метод search не получил аргументов для поиска')

    async def get_all_tags(self) -> list[str]:
        """
        Метод возвращает список всех tags
        упомянутых на сайте

        :return:
        """
        url = f'{self._host}/tags'
        raw_tags = (await self.__get_site_content(url)).find_all('li', class_='sidetag')
        tags = [tag.find_all('a')[-1].text.replace(' ', '_') for tag in raw_tags]

        return tags

    async def random(self, count) -> list[Manga]:
        url = f'{self._host}/manga/random'
        return await self.__get_search_content(url, count)

    async def get_manga(self, manga_id: str) -> Manga:
        """
        Метод возвращает объект Manga

        :param manga_id:
        :return:
        """
        url = f'{self._host}/manga/{manga_id}.html'
        content = await self.__get_site_content(url)

        dle_content = content.find('div', id='content').find('div', id='dle-content')
        side_content = content.find('div', id='side')

        m = Manga(id=manga_id)
        m.poster = dle_content.find('div', id='manga_images').find('img').attrs.get('src')
        m.title = dle_content.find('div', id='info_wrap').find('a', class_='title_top_a').string
        m.date = dle_content.find('div', class_='row4_right').find('b').string

        info_rows = dle_content.find('div', id='info_wrap').find_all('div', class_='row')
        for el in info_rows:
            if el.find('div', class_='item').string == 'Аниме/манга':
                m.series = el.find('a').string
            elif el.find('div', class_='item').string == 'Автор':
                m.author = el.find('a').string
            elif el.find('div', class_='item').string == 'Переводчик':
                m.translator = el.find('a').string

        tags = []
        tags_table = side_content.find_all('li', class_='sidetag')
        for tag in tags_table:
            tags.append(((tag.find_all('a'))[-1]).string.replace(' ', '_'))

        m.tags = tags
        m.original_url = f'{self._host}/online/{m.id}.html'
        m.content = await self.__get_manga_content(m)
        return m

    async def __get_search_content(self, url: str, count: int, offset: int = 20, params: dict = {}) -> list[Manga]:
        """
        Вспомогательный метод, используется для парсинга манги из поисковой выдачи

        :param url:
        :param offset:
        :param params: params для url
        :return:
        """
        soup_content = await self.__get_site_content(url, params={**params, 'offset': offset})
        elements = soup_content.find('div', id='content').find_all('div', class_='content_row')[:count]

        content = []
        for el in elements:
            el_div_with_manga_id = el.find('div', class_='manga_row1')
            if el_div_with_manga_id.find('a', class_='title_link'):
                href = el_div_with_manga_id.find('a', class_='title_link').attrs.get('href')
            else:
                href = el_div_with_manga_id.find('a').attrs.get('href').replace(self._host, '')

            _id = re.search(r'/(.+)/(.+).html', href)
            if _id.group(1) == 'manga':
                content.append(_id.group(2))

        manga_list = await asyncio.gather(*(self.get_manga(manga_id) for manga_id in content))
        return manga_list

    async def __get_manga_content(self, manga: Manga) -> MangaContent:
        """
        Вспомогательный метод для парсинга контента манги

        :param manga: Manga class
        :return:
        """
        return MangaContent(get_site_content_method=self.__get_site_content, manga=manga)
