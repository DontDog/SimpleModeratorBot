from app import FILENAME_LOG
from aiogram.types import FSInputFile
from aiogram import Router, types

router = Router()


@router.message(lambda message: message.chat.type == "private" and message.text == "/save")
async def save_people(message: types.Message):

    await message.answer_document(document=FSInputFile(FILENAME_LOG),
                                  caption="Вот log.")