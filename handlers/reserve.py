from aiogram import Router, types
from db import User, Schedule, State
from app import GROUP_CHAT_ID, PRESENCE_CHECK_START, PRESENCE_CHECK_END
from datetime import datetime

router = Router()


@router.message(lambda message: message.chat.type == "supergroup"
                                and datetime.strptime(PRESENCE_CHECK_START,"%H:%M").time() <=
                                datetime.now().time() <= datetime.strptime(PRESENCE_CHECK_END, "%H:%M").time()
                                and message.chat and message.chat.id == GROUP_CHAT_ID
                                and message.text and message.text.lower().startswith("тут"))
async def reserve_room(message: types.Message):
    user_id = message.from_user.id
    u = User.get_by_telegram_id(user_id)
    State.set('del', f'{message.message_id}')
    if not u:
        await message.reply('Вы не зарегистрированы. Сначала зарегистрируйтесь, отправив ваше "!Фамилия", без кавычек.')
        return

    s = Schedule.get_by_user(user_id)
    if len(s) == 0:
        await message.reply(f"ОШИБКА! Возможно Вы отмечаетесь не по расписанию!")
        return

    if u.last_checked and u.last_checked:
        await message.reply(f"Ваше присутствие уже отмечено в аудитории {s[0].room}.")
        return

    m = await message.reply(f"Ваше присутствие отмечено в аудитории {s[0].room}.")
    State.set('del', f'{m.message_id}')
    User.update_last_checked(user_id)