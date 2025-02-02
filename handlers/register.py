from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

# Словарь для хранения преподавателей
teachers_db = {}


@router.message(lambda message: message.chat.type == "supergroup")
async def register_teacher(message: types.Message):
    full_name = message.text.strip()
    username = message.from_user.username
    user_id = message.from_user.id

    if user_id in teachers_db:
        await message.reply("Вы уже зарегистрированы!")
        return

    teachers_db[user_id] = {"name": full_name, "username": username}
    await message.reply(f"Регистрация успешна! {full_name}, ваш username: @{username}")

