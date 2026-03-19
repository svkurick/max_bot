from importlib.metadata import files

import httpx
import os

class MaxClient:

    def __init__(self, token: str, base_url="https://platform-api.max.ru"):
        self.base_url = base_url
        self.token = token
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=10.0,
                read=60.0,
                write=10.0,
                pool=10.0
            )
        )

    async def request(
            self,
            method: str,
            path: str,
            json=None,
            params=None,
            files=None,
            data=None,
            type_param=None,
            base_url_blank=False
    ) -> dict:
        headers = {
            "Authorization": self.token
        }
        if type_param:
            params = {'type': type_param}

        if base_url_blank:
            path_url = path
        else:
            path_url = f"{self.base_url}{path}"

        r = await self.client.request(
            method,
            path_url,
            json=json,
            params=params,
            files=files,
            data=data,
            headers=headers
        )

        r.raise_for_status()
        return r.json()
