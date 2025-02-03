from app import teachers_db
from aiogram.types import FSInputFile
from aiogram import Router, types

router = Router()


@router.message(lambda message: message.chat.type == "supergroup" and message.text == "/save")
async def save_people(message: types.Message):
    await message.answer_document(document=FSInputFile(teachers_db.filename), caption="Вот список зарегистрированных преподавателей.")