from app import teachers_db, schedule_db, bot
from app.config import GROUP_CHAT_ID

async def send_statistics():
    """Функция для отправки статистики в группу."""
    rooms = schedule_db.get_teachers_by_day()

    # Сообщение с пользователями, которые отметились
    checked_message = "Сегодня отметились:\n"
    for room in rooms:
        if teachers_db.check_user_by_full_name(room['teacher']):
            checked_message += f"{room['teacher']} ({room['room']}): +\n"

    # Сообщение с пользователями, которые не отметились
    not_checked_message = "\nНе отметились:\n"
    for room in rooms:
        if not teachers_db.check_user_by_full_name(room['teacher']):
            not_checked_message += f"{room['room']} ({room['teacher']}): -\n"
    # Отправляем первое сообщение с пользователями, которые отметились
    await bot.send_message(GROUP_CHAT_ID, checked_message)

    # Отправляем второе сообщение с пользователями, которые не отметились
    await bot.send_message(GROUP_CHAT_ID, not_checked_message)