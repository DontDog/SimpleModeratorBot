from aiogram import Router, types
from app import teachers_db

router = Router()


@router.message(lambda message: message.chat.type == "supergroup" and message.text.lower().startswith("тут"))
async def reserve_room(message: types.Message):
    user_id = message.from_user.id

    if not teachers_db.get_user(user_id):
        await message.reply("Вы не зарегистрированы. Сначала зарегистрируйтесь, отправив ваше ФИО.")
        return

    teacher_name = teachers_db.get_user(user_id)["name"]
    await message.reply(f"{teacher_name}, Ваше присутствие отмечено.")