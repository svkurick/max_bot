import asyncio
import httpx


async def run_polling(bot, dispatcher):

    offset = 0
    print("🤖 Бот запущен, ожидаю сообщения...")

    while True:
        try:
            updates = await bot.client.request(
                "GET",
                f"/updates?offset={offset}"
            )

            # Извлекаем marker и updates из ответа
            if isinstance(updates, dict):
                marker = updates.get("marker")
                updates = updates.get("updates", [])
                if marker:
                    offset = marker

            # Если пусто — пропускаем
            if not updates:
                await asyncio.sleep(1)
                continue

            for update in updates:
                await dispatcher.process_update(update)

        except httpx.ReadTimeout:
            continue

        except Exception as e:
            print("Polling error:", e)
            await asyncio.sleep(1)
