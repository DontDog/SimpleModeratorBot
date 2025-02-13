from aiogram import Router, types

router = Router()

@router.message(lambda message: message.text == "//info//")
async def start_command(message: types.Message):
    await message.answer(f"{message}")