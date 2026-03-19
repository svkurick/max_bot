import asyncio
import httpx


async def run_polling(bot, dispatcher):

    offset = 0

    while True:
        try:
            updates = await bot.client.request(
                "GET",
                f"/updates?offset={offset}"
            )

            # Если updates — словарь с ключом "updates"
            if isinstance(updates, dict) and "updates" in updates:
                updates = updates["updates"]

            # Если пусто — пропускаем
            if not updates:
                await asyncio.sleep(1)  # небольшой sleep чтобы не грузить CPU
                continue

            for update in updates:
                await dispatcher.process_update(update)

                # Защита: убедимся, что update_id есть
                if "update_id" in update:
                    offset = update["update_id"] + 1

        except httpx.ReadTimeout:
            # нормальное поведение long polling
            continue

        except Exception as e:
            print("Polling error:", e)
            await asyncio.sleep(1)  # маленькая пауза, чтобы не спамить
