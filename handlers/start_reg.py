from app import flag_registration
from aiogram import Router, types, F

router = Router()


@router.message(lambda message: message.chat.type == "private" and message.text == '/start_reg')
async def start_reg(message: types.Message):
    flag_registration.set(True)
    await message.reply(f"Регистрация запущена.")


@router.message(lambda message: message.chat.type == "private" and message.text == '/stop_reg')
async def stop_reg(message: types.Message):
    flag_registration.set(False)
    await message.reply(f"Регистрация остановлена.")
