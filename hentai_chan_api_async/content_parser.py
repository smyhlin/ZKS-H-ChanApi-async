import json
import re

from aiograph import Telegraph


class MangaContent:
    def __init__(self, get_site_content_method, manga):
        self.__get_site_content = get_site_content_method
        self._Manga = manga

    async def images(self) -> list[str]:
        soup_content = await self.__get_site_content(self._Manga.original_url, params={'development_access': 'true'})
        raw_js = soup_content.find_all('script')[2].text

        var_data = raw_js.replace('createGallery(data)', '').replace('    ', '').replace('\n', '').replace("'", '"')
        pattern = re.compile(r"var data = (\{.*?\})$", re.MULTILINE | re.DOTALL)

        if var_data:
            obj = pattern.search(var_data).group(1)
            obj = json.loads(obj)
            return obj['fullimg']
        else:
            return []

    async def as_telegraph(self,
                           short_name: str = 'HentaiChan',
                           author_name: str = 'JKearnsl',
                           author_url: str = 'https://t.co/JKearnsl',
                           title: str = None,
                           description: str = None,
                           token: str = None
                           ) -> str:
        telegraph = Telegraph(token=token)

        images = await self.images()
        html_manga_content = [f'<img src="{image}"/>' for image in images]
        description_content = '' if not description else description

        await telegraph.create_account(short_name, author_name, author_url)
        page = await telegraph.create_page(
            title=(self._Manga.title if not title else title)[:256],
            content=f'{description_content}\n{"".join(html_manga_content)}',
            author_name=author_name,
            author_url=author_url,
            access_token=token
        )
        await telegraph.close()
        return page.url