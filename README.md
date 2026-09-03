# pymaxbot

Python SDK для создания ботов в мессенджере [MAX](https://max.ru).

## Установка

```bash
pip install pymaxbot
```

## Быстрый старт

```python
import asyncio
from max_bot import Bot, Dispatcher, run_polling

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher(bot)


@dp.message(commands=["start"])
async def start(msg):
    await msg.answer("Привет! Я эхо-бот.")


@dp.message()
async def echo(msg):
    await msg.answer(f"Вы написали: {msg.text}")


asyncio.run(run_polling(bot, dp))
```

## Возможности

- Отправка текстовых сообщений с поддержкой HTML-форматирования
- Inline-кнопки и обработка callback-нажатий
- Отправка изображений (одно или несколько)
- Отправка файлов/документов
- Удаление сообщений
- Маршрутизация по командам и payload-ам через `Dispatcher`
- Long polling из коробки

## Примеры

### Inline-кнопки

```python
@dp.message(commands=["menu"])
async def menu(msg):
    await msg.answer(
        "Выберите вариант:",
        buttons=[
            [{"text": "Вариант А", "payload": "option_a"},
             {"text": "Вариант Б", "payload": "option_b"}],
            [{"text": "Отмена", "payload": "cancel"}],
        ]
    )


@dp.callback(payloads=["option_a", "option_b"])
async def on_option(cb):
    await cb.answer()
    await cb.reply(f"Вы выбрали: <b>{cb.payload}</b>", format="html")
```

### Отправка изображений

```python
@dp.message(commands=["photo"])
async def photo(msg):
    await msg.send_image("image.jpg", text="Подпись к фото")
```

### Отправка файлов

```python
@dp.message(commands=["doc"])
async def doc(msg):
    await msg.send_document("report.pdf")
```

### Удаление сообщения

```python
@dp.message(commands=["del"])
async def delete(msg):
    sent = await msg.answer("Удалится через 3 секунды...")
    await asyncio.sleep(3)
    await sent.delete()
```

## Ссылки

- [Репозиторий на GitHub](https://github.com/svkurick/max_bot)
- [Сообщить об ошибке](https://github.com/svkurick/max_bot/issues)