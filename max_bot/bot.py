import os
import httpx
import time

from .client import MaxClient
from .types.message import Message


class Bot:

    def __init__(self, token: str):
        self.client = MaxClient(token)

    async def send_message(self, chat_id: int, text: str, format=None):
        if format:
            json = {
                "text": text,
                "format": format
            }
        else:
            json = {
                "text": text
            }
        params = {"user_id": chat_id}

        data = await self.client.request(
            "POST",
            f"/messages",
            json=json,
            params=params
        )
        return Message(data['message'], self)


    async def upload_file(self, file_path: str):
        r = await self.client.request('POST', '/uploads', type_param='file')
        upload_url = r.get('url')

        with open(file_path, "rb") as f:
            files = {
                "data": (os.path.basename(file_path), f)
            }

            return await self.client.request(
                "POST",
                upload_url,
                files=files,
                base_url_blank=True
            )


    async def send_documents(self, chat_id: int, file_path: list[str]):

        for path in file_path:
            # 1️⃣ загружаем файл
            upload = await self.upload_file(path)
            file_token = upload["token"]

            # 2️⃣ отправляем
            json = {
                "attachments": [
                    {
                        "type": "file",
                        "payload": {
                            "token": file_token
                        }
                    }
                ]
            }

            params = {"user_id": chat_id}

            time.sleep(2)


            await self.client.request(
                "POST",
                "/messages",
                json=json,
                params=params
            )


    async def send_document(self, chat_id: int, file_path: str):

        upload = await self.upload_file(file_path)
        file_token = upload["token"]

        json = {
            "attachments": [
                {
                    "type": "file",
                    "payload": {
                        "token": file_token
                    }
                }
            ]
        }

        params = {"user_id": chat_id}

        time.sleep(2)

        data = await self.client.request(
            "POST",
            "/messages",
            json=json,
            params=params
        )

        return Message(data['message'], self)

    async def delete_message(self, mid: str):

        params = {"message_id": mid}
        res = await self.client.request(
            "DELETE",
            f"/messages",
            params=params
        )
        return res
