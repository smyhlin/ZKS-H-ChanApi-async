import re

from bs4 import BeautifulSoup

from ..data import Manga


def parse_manga(bs_content: BeautifulSoup, manga_id: str, host: str) -> Manga:
    """
    Метод возвращает объект Manga без поля 'content'

    :param host:
    :param bs_content:
    :param manga_id:
    :return:
    """

    dle_content = bs_content.find('div', id='content').find('div', id='dle-content')
    side_content = bs_content.find('div', id='side')

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
    m.original_url = f'{host}/online/{m.id}.html'
    return m


def parse_manga_ids(bs_content: BeautifulSoup, count: int, host: str) -> list[str]:
    """
    Вспомогательный метод, используется для парсинга id манги из поисковой выдачи

    :param host:
    :param bs_content: BeautifulSoup content
    :param count:
    :return: list[manga_ids]
    """
    elements = bs_content.find('div', id='content').find_all('div', class_='content_row')[:count]

    content = []
    for el in elements:
        el_div_with_manga_id = el.find('div', class_='manga_row1')
        if el_div_with_manga_id.find('a', class_='title_link'):
            href = el_div_with_manga_id.find('a', class_='title_link').attrs.get('href')
        else:
            href = el_div_with_manga_id.find('a').attrs.get('href').replace(host, '')

        _id = re.search(r'/(.+)/(.+).html', href)
        if _id.group(1) == 'manga':
            content.append(_id.group(2))

    return content


def parse_tags(bs_content: BeautifulSoup) -> list[str]:
    """
    Возвращает список всех существующих тегов

    :param bs_content:
    :return:
    """
    div = bs_content.find('span', class_='news')
    raw_tags = div.find_all('a')
    tags = [tag.text for tag in raw_tags]

    return tags
