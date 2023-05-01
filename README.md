[![PyPI version](https://badge.fury.io/py/hentai-chan-api-async.svg)](https://badge.fury.io/py/hentai-chan-api-async)
![PyPI - License](https://img.shields.io/pypi/l/hentai-chan-api-async)
[![CodeFactor](https://www.codefactor.io/repository/github/jkearnsl/hentaichanapi-async/badge)](https://www.codefactor.io/repository/github/jkearnsl/hentaichanapi-async)


# HentaiChanApi-async
## Wrapper over https://hentaichan.live

hentai-chan-api-async is a small asynchronous parser library 
that will allow you to easily use manga from https://hentaichan.live
Recommended to use python3.7+

Sync version: [@HentaiChanApi](https://github.com/JKearnsl/HentaiChanApi) - archived

## Install

```sh
pip install hentai-chan-api-async
```

## Features

- Parsing by pages and quantities
- Search engine by queries and by tags
- Manga object to easily retrieve manga data
- Ability to use a proxy
- Asynchronous

## Examples

An example of using the 'get_new' method:
```Python
import asyncio
from hentai_chan_api_async import HentaiChan


async def main():
    hc = HentaiChan()

    manga = await hc.get_new(page_num=1, count=2)

    for el in manga:
        print(el.id)  # '40918-doll-house-glava-2'
        print(el.title)  # 'Doll House - глава 2'
        print(el.poster)  # https://imgcover.../.../01.jpg'
        print(el.series)  # 'Оригинальные работы'
        print(el.author)  # 'Sexgazers'
        print(el.translator)  # 'Zone'
        print(await el.content.images())  # ['https://.../.png', 'https://.../.png'...]
        print(el.tags)  # ['анал', 'без цензуры', 'большая грудь', ...]
        print(el.date)  # '17 января 2022'
        print(el.original_url) # 'https://...'


asyncio.get_event_loop().run_until_complete(main())
    
```
Note that the arguments: "page_num=1" and "count=2" are optional.
By default, "page_num=1" and "count=20".

Also note that calling "el.content.images" will invoke the parser, which may take some time to use. I advise you to call "el.content.images" only when necessary.


Tag search example:
```Python
import asyncio
from hentai_chan_api_async import HentaiChan


async def main():
    hc = HentaiChan()

    tags = await hc.tags()  # ['3D', 'action', 'ahegao', 'bdsm', 'corruption', ...]
    manga = await hc.search(tag=tags[0])  # [Manga(id='40779-ms-i', title='Ms. I (Невыразимые секреты её прошлого)')...]

    print(manga[0].title)  # Ms. I (Невыразимые секреты её прошлого)
    print(await manga[0].content.images())  # ['https://mimg2.imgschan.xyz/manganew/m/1641154521_ms.-i/001.jpg', ...]


asyncio.get_event_loop().run_until_complete(main())

```

Search query example:
```Python
import asyncio
from hentai_chan_api_async import HentaiChan


async def main():
    hc = HentaiChan()
    manga = await hc.search(query='bikini')  # [Manga(...)...]
    
    print(manga[0].title)  # Bikini's Bottom
    print(await manga[0].content.images())  # ['https://mimg2.imgschan.xyz/manganew/l/1630962513_lightsource-bik...', ...]


asyncio.get_event_loop().run_until_complete(main())
```

Get manga by id method example with new related funciton example:
```Python
import asyncio
from zkshentai_chan_api_async import HentaiChan


async def main():
    hc = HentaiChan()

    id = '41136-ledi-k-i-podavlennyy-muzhchina-glava-15'
    el = await hc.manga(id)

    print(el.id)  # '40918-doll-house-glava-2'
    print(el.title)  # 'Леди К и Подавленный Мужчина - Глава 1.5 (Kko to yamioji)'
    print(el.poster)  # https://imgcover.../.../01.jpg'
    print(el.series)  # 'Оригинальные работы'
    print(el.author)  # 'Rororogi Mogera'
    print(el.translator)  # 'Amunezqa'

    # HentaiChan Very clever and naming their 1.5 chapters url`s as 15
    print(el.related)  # ['https://.../glava-1.html', 'https://.../glava-15.html', 'https://.../glava-2.html'...]
    # But when it is over 20+ chapters related chapters parser due to async work get unsorted list so...
    # Under 15 chapters sort unneeded
    el_sorted = await hc.manga(id, rel_sort=True)
    print(el_sorted.related) # ['https://.../glava-1.html', 'https://.../glava-2.html'... 'https://.../glava-15.html'...]

    # print(await el.content.images())  # ['https://.../.png', 'https://.../.png'...]
    print(el.tags)  # ['анал', 'без цензуры', 'большая грудь', ...]
    print(el.date)  # '07 февраля 2022'
    print(el.original_url) # 'https://...'


asyncio.get_event_loop().run_until_complete(main())

```
