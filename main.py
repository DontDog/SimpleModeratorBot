import asyncio
from aiogram import Dispatcher
from app import bot, scheduler
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_teacher, start, reserve, save, set, send_statistics


async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start.router)
    dp.include_router(save.router)
    dp.include_router(set.router)
    dp.include_router(register_teacher.router)
    dp.include_router(reserve.router)

    scheduler.add_job(send_statistics, 'cron', hour=17, minute=50, day_of_week='0-5')
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())