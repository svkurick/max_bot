from ..types.message import Message


class Dispatcher:

    def __init__(self, bot):
        self.bot = bot
        self.handlers = []

    def message(self, commands=None):
        def decorator(func):
            self.handlers.append({
                "func": func,
                "commands": commands,
            })
            return func

        return decorator

    async def process_update(self, update):

        if "message" not in update:
            return
        message = Message(update["message"], self.bot)
        for handler in self.handlers:
            commands = handler["commands"]
            if commands:
                if not message.text:
                    continue

                if not any(
                        message.text.startswith(f"/{cmd}")
                        for cmd in commands
                ):
                    continue

            try:
                await handler["func"](message)
                break
            except Exception as e:
                print("❌ Handler error:", e)