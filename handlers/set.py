from db import Schedule
from aiogram import Router, types, F

router = Router()


@router.message(lambda message: message.document and message.chat.type == "private" and message.caption == '/set')
async def set_schedule(message: types.Message):

    file_id = message.document.file_id
    file_name = message.document.file_name
    file = await message.bot.get_file(file_id)
    await message.bot.download(file, destination=f"./downloads/{file_name}")
    Schedule.load_schedule_from_excel(f"./downloads/{file_name}")
    await message.reply(f"Расписание обновлено.")
