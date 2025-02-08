from app import teachers_db, schedule_db
from aiogram.types import FSInputFile
from aiogram import Router, types

router = Router()


@router.message(lambda message: message.chat.type == "private" and message.text == "/save")
async def save_people(message: types.Message):
    await message.answer_document(document=FSInputFile(teachers_db.filename),
                                  caption="Вот список зарегистрированных преподавателей.")
    await message.answer_document(document=FSInputFile(schedule_db.filename),
                                  caption="Вот расписание занятий.")