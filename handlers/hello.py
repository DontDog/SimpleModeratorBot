from app import bot
from app.config import GROUP_CHAT_ID

async def send_hello():
    await bot.send_message(GROUP_CHAT_ID, "Бот начинает работу!")

