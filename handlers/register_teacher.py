from app import teachers_db
from aiogram import Router, types

router = Router()

@router.message(lambda message: message.chat.type == "supergroup" and message.text and message.text.startswith("!"))
async def register_teacher(message: types.Message):
    full_name = message.text[1:].strip()
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_username = message.from_user.username


    if teachers_db.get_user(user_id):
        d = teachers_db.get_user(user_id)
        await message.reply(f'Вы изменили имя с "{d["name"]}", на "{full_name}"')

    teachers_db.add_or_update_user(user_id, full_name, user_full_name, user_username)
    await message.reply(f"Регистрация прошла успешно! {full_name}")
