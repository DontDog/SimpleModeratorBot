import asyncio
from aiogram import Dispatcher
from app.bot import bot
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_teacher, start, reserve, save


def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start.router)
    dp.include_router(save.router)
    dp.include_router(register_teacher.router)
    dp.include_router(reserve.router)

    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()