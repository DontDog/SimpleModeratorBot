from datetime import datetime

from app import bot, FILENAME_LOG
from app.config import GROUP_CHAT_ID
from db import Schedule, User

async def send_statistics(log = False):
    """Функция для отправки статистики в группу."""
    teachers = Schedule.get_teachers_by_day()
    current_time = datetime.now().strftime("%d.%m.%Y")
    # Сообщение с пользователями, которые отметились
    checked_message = f"Сегодня отметились({current_time}):\n"
    for teacher in teachers:
        if User.check_user(teacher['id']):
            checked_message += f"{teacher['name']} ({teacher['room']}): +\n"

    # Сообщение с пользователями, которые не отметились
    not_checked_message = f"\nНе отметились({current_time}):\n"
    for teacher in teachers:
        if not User.check_user(teacher['id']):
            not_checked_message += f"{teacher['room']} ({teacher['name']}): -\n"

    if log:
        with open(FILENAME_LOG, "a", encoding="utf-8") as file:
            file.write("\n--------------------------------------"
                       "----------------------------------------\n")
            file.write(checked_message + "\n\n")
            file.write(not_checked_message + "\n")
    else:
        # Отправляем первое сообщение с пользователями, которые отметились
        await bot.send_message(GROUP_CHAT_ID, checked_message)

        # Отправляем второе сообщение с пользователями, которые не отметились
        await bot.send_message(GROUP_CHAT_ID, not_checked_message)

