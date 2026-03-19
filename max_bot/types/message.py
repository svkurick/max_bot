class Message:

    def __init__(self, data, bot):
        self.data = data
        self.bot = bot

        body = data.get("body") or {}

        self.text = body.get("text")
        self.mid = body.get("mid")

        sender = data.get("sender") or {}
        self.chat_id = sender.get("user_id")

    async def answer(self, text):
        if not self.chat_id:
            # просто игнорируем, если некуда писать
            return
        return await self.bot.send_message(chat_id=self.chat_id, text=text)

    async def send_document(self, file_path):
        if not self.chat_id:
            return
        await self.bot.send_document(chat_id=self.chat_id, file_path=file_path)

    async def send_documents(self, file_path):
        if not self.chat_id:
            return
        await self.bot.send_documents(chat_id=self.chat_id, file_path=file_path)

    async def delete(self):
        if self.mid:
            try:
                await self.bot.delete_message(self.mid)
            except:
                pass
