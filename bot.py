import os
import asyncio
import logging
import httpx
from aiogram import Bot, Dispatcher, types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("Не найден BOT_TOKEN")
    raise SystemExit("BOT_TOKEN не установлен")

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

TRANSLATE_URL = "https://libretranslate.de/translate"

async def translate_text(text: str, target_lang: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TRANSLATE_URL,
            data={
                "q": text,
                "source": "auto",
                "target": target_lang,
                "format": "text"
            },
            timeout=15
        )
        data = response.json()
        return data.get("translatedText", "")

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! 👋\nЯ бот-переводчик 🇰🇿 ⇄ 🇷🇺\nПросто отправь текст на казахском или русском."
    )

@dp.message_handler(content_types=types.ContentType.TEXT)
async def translate_message(message: types.Message):
    text = message.text.strip()
    if not text:
        await message.reply("Пустое сообщение — пришли текст для перевода.")
        return

    if any("\u0400" <= c <= "\u04FF" for c in text):
        target_lang = "kk"
        flag = "🇷🇺 ➜ 🇰🇿"
    else:
        target_lang = "ru"
        flag = "🇰🇿 ➜ 🇷🇺"

    try:
        translated = await translate_text(text, target_lang)
        await message.reply(f"{flag}\n{translated}")
    except Exception as e:
        logger.exception("Ошибка при переводе")
        await message.reply("Произошла ошибка при переводе. Попробуй позже.")

async def main():
    logger.info("Бот запущен ✅ Жду сообщений...")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
