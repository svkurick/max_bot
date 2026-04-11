import httpx
import asyncio

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
            base_url_blank=False,
            max_retries=5,
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

        delay = 1

        for attempt in range(max_retries):
            r = await self.client.request(
                method,
                path_url,
                json=json,
                params=params,
                files=files,
                data=data,
                headers=headers
            )
            try:
                data_resp = r.json()
            except Exception:
                data_resp = {}

                # 🔥 проверка attachment.not.ready
            if (
                isinstance(data_resp, dict)
                and data_resp.get("code") == "attachment.not.ready"
            ):
                print(f"⏳ attachment not ready, retry {attempt + 1}, sleep {delay}s")
                await asyncio.sleep(delay)
                delay += 3
                continue

            # если статус плохой — падаем
            if r.is_error:
                print(f"❌ HTTP {r.status_code} response body:", r.text)
            r.raise_for_status()

            return data_resp

        raise Exception("❌ Превышено количество попыток (attachment not ready)")
