import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from googletrans import Translator

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
translator = Translator()

@dp.message_handler()
async def translate_message(message: types.Message):
    text = message.text
    try:
        lang = translator.detect(text).lang
        if lang == "ru":
            dest = "kk"
        else:
            dest = "ru"
        translated = translator.translate(text, dest=dest).text
        await message.reply(translated)
    except Exception as e:
        await message.reply(f"Ошибка перевода: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
