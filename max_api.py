import asyncio
import httpx
import configparser
from dotenv import load_dotenv

load_dotenv()


def load_config(path: str):
    config = configparser.RawConfigParser()
    config.read(path)
    return config


BASE_URL = "https://platform-api.max.ru"


config = load_config('config.properties')
token = config.get('bot', 'token')
ADMIN_CHAT_ID = config.get('bot', 'admin_chat_id')
ADMIN_CHAT_ID = 3974670

HEADERS = {
    "Authorization": token,
    "Content-Type": "application/json"
}


class MaxBot:
    def __init__(self):
        self.offset = None

    # ─── API ──────────────────────────────────────

    async def get_updates(self):
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{BASE_URL}/updates",
                headers=HEADERS,
                params={"offset": self.offset}
            )
            resp.raise_for_status()
            return resp.json()["updates"]

    async def send_message(self, user_id: int, text: str, format=None):
        async with httpx.AsyncClient() as client:
            if format:
                body = {
                        "text": text,
                        "format": format
                    }
            else:
                body = {
                        "text": text
                    }
            resp = await client.post(
                f"{BASE_URL}/messages",
                headers=HEADERS,
                json={
                    "recipient": {
                        "user_id": user_id
                    },
                    "body": body
                }
            )

            if resp.status_code != 200:
                print("❌ send_message error:", resp.status_code, resp.text)

    async def forward_to_admin(self, update: dict):
        message = update.get("message")
        if not message:
            return

        mid = message["body"].get("mid")
        if not mid:
            return

        await self.forward_message(ADMIN_CHAT_ID, mid)

    async def forward_message(self, to_chat_id: int, mid: str):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/messages",
                headers=HEADERS,
                json={
                    "recipient": {
                        "user_id": to_chat_id
                    },
                    "forward": {
                        "mid": mid
                    }
                }
            )
            resp.raise_for_status()

    # ─── HANDLERS ─────────────────────────────────

    async def handle_message(self, update: dict):
        message = update["message"]
        chat_id = message["sender"]["user_id"]
        text = message['body'].get("text", "")

        print(f"📩 {chat_id}: {text}")

        # простой echo
        await self.send_message(chat_id, f"Вы написали: {text}")

    async def handle_update(self, update: dict):
        if update.get("update_type") == "message_created":
            await self.forward_to_admin(update)

    # ─── POLLING ──────────────────────────────────

    async def polling(self):
        print("🤖 MAX bot started (long polling)")
        while True:
            try:
                updates = await self.get_updates()

                for upd in updates:
                    self.offset = upd["message"]["body"]["seq"] + 1
                    await self.handle_update(upd)

            except Exception as e:
                print("⚠️ error:", e)
                await asyncio.sleep(2)


if __name__ == "__main__":
    bot = MaxBot()
    asyncio.run(bot.polling())