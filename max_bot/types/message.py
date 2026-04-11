class Message:

    def __init__(self, data, bot):
        self.data = data
        self.bot = bot

        body = data.get("body") or {}

        self.text = body.get("text")
        self.mid = body.get("mid")

        sender = data.get("sender") or {}
        self.chat_id = sender.get("user_id")

        recipient = data.get("recipient") or {}
        self.dialog_chat_id = recipient.get("chat_id")

    async def answer(self, text: str, format=None, buttons=None):
        if not self.chat_id:
            return
        return await self.bot.send_message(chat_id=self.chat_id, text=text, format=format, buttons=buttons)

    async def send_document(self, file_path: str):
        if not self.chat_id:
            return
        await self.bot.send_document(chat_id=self.chat_id, file_path=file_path)

    async def send_documents(self, file_path: list[str]):
        if not self.chat_id:
            return
        await self.bot.send_documents(chat_id=self.chat_id, file_path=file_path)

    async def send_image(self, file_path: str, text: str = None):
        if not self.chat_id:
            return
        return await self.bot.send_image(chat_id=self.chat_id, file_path=file_path, text=text)

    async def send_images(self, file_paths: list[str], text: str = None):
        if not self.chat_id:
            return
        await self.bot.send_images(chat_id=self.chat_id, file_paths=file_paths, text=text)

    async def delete(self):
        if self.mid:
            try:
                await self.bot.delete_message(self.mid)
            except Exception:
                pass