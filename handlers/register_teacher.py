from app import GROUP_CHAT_ID
from db import User, State
from aiogram import Router, types

router = Router()

@router.message(lambda message: message.chat.type == "supergroup"
                                and message.chat and message.chat.id == GROUP_CHAT_ID
                                and message.text and message.text.startswith("!"))
async def register_teacher(message: types.Message):
    full_name = message.text[1:].strip()
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_username = message.from_user.username

    u = User.get_by_telegram_id(user_id)
    if u:
        User.update_user(user_id=u.id,
            name=full_name,
            full_name=user_full_name,
            username=user_username,
            telegram_id=user_id)
        await message.reply(f'Вы изменили имя с "{u.name}", на "{full_name}"')

    User.create(
        name=full_name,
        full_name=user_full_name,
        username=user_username,
        telegram_id=user_id)

    await message.reply(f"Регистрация прошла успешно!")

@router.message(lambda message: message.chat.type == "private" and message.text == '/start_reg')
async def start_reg(message: types.Message):

    if State.get('flag') is not None and State.get('flag')[0] == 'True':
        await message.reply(f"Регистрация уже запущена.")
        return

    if State.get('flag') is not None:
        State.remove('flag')
    State.set('flag', 'True')
    await message.reply(f"Регистрация запущена.")


@router.message(lambda message: message.chat.type == "private" and message.text == '/stop_reg')
async def stop_reg(message: types.Message):
    if State.get('flag') is not None and State.get('flag')[0] == 'False':
        await message.reply(f"Регистрация уже остановлена.")
        return
    if State.get('flag') is not None:
        State.remove('flag')
    State.set('flag', 'False')
    await message.reply(f"Регистрация остановлена.")
