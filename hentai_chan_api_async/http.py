import aiohttp


class Http:
    def __init__(self, headers: dict = None):
        self.headers = headers

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def get(self, url, proxy: dict = None, params: dict = None):
        async with self._session.get(url, proxy=proxy, params=params) as resp:
            resp.raise_for_status()
            return await resp.text('utf-8')
