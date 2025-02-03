from aiogram import Router, types
from app import teachers_db, schedule_db

router = Router()


@router.message(lambda message: message.chat.type == "supergroup" and message.text and message.text.lower().startswith("тут"))
async def reserve_room(message: types.Message):
    user_id = message.from_user.id

    if not teachers_db.get_user(user_id):
        await message.reply("Вы не зарегистрированы. Сначала зарегистрируйтесь, отправив ваше ФИО.")
        return

    teacher_name = teachers_db.get_user(user_id)["name"]
    row = schedule_db.find_schedule(teacher_name)
    if len(row) == 0:
        await message.reply(f"{teacher_name}, Вы сегодня не преподаёте.")

    room = row[0]['room']
    last_check = teachers_db.check_user_by_full_name(teacher_name)
    if last_check:
        await message.reply(f"{teacher_name}, Ваше присутствие уже отмечено в аудитории {room}.")
        return

    await message.reply(f"{teacher_name}, Ваше присутствие отмечено в аудитории {room}.")
    teachers_db.update_last_checked(user_id)