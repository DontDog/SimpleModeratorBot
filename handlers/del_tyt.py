from app import bot
from app.config import GROUP_CHAT_ID

from db import State
import time

async def del_tyt():
    await bot.send_message(GROUP_CHAT_ID, "Бот удаляет все сообщения!")
    for msg in State.get('del'):
        await bot.delete_message(GROUP_CHAT_ID, int(msg))
        time.sleep(1)

