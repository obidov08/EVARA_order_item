from decouple import config
from aiogram import Bot

BOT_TOKEN = config('BOT_TOKEN')
ADMIN_ID = config("ADMIN_ID")


async def send_message(text):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=ADMIN_ID, text=text)
    bot.close() 
      