from ..types.message import Message
from ..types.callback import Callback


class Dispatcher:

    def __init__(self, bot):
        self.bot = bot
        self.handlers = []
        self.callback_handlers = []

    def message(self, commands=None):
        def decorator(func):
            self.handlers.append({
                "func": func,
                "commands": commands,
            })
            return func
        return decorator

    def callback(self, payloads=None):
        def decorator(func):
            self.callback_handlers.append({
                "func": func,
                "payloads": payloads,
            })
            return func
        return decorator

    async def process_update(self, update):
        update_type = update.get("update_type")

        if update_type == "message_callback":
            await self._process_callback(update)
        elif "message" in update:
            await self._process_message(update["message"])

    async def _process_message(self, raw_message: dict):
        message = Message(raw_message, self.bot)
        for handler in self.handlers:
            commands = handler["commands"]
            if commands:
                if not message.text:
                    continue
                cmd_word = message.text.split()[0]
                if not any(cmd_word == f"/{cmd}" for cmd in commands):
                    continue
            try:
                await handler["func"](message)
                break
            except Exception as e:
                print("❌ Handler error:", e)

    async def _process_callback(self, update: dict):
        cb = Callback(update, self.bot)
        for handler in self.callback_handlers:
            payloads = handler["payloads"]
            if payloads and cb.payload not in payloads:
                continue
            try:
                await handler["func"](cb)
                break
            except Exception as e:
                print("❌ Callback handler error:", e)