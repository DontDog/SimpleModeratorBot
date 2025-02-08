import asyncio
from aiogram import Dispatcher
from app import bot, scheduler
from app.config import PRESENCE_REPORT, PRESENCE_REPORT_LOG
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import (register_teacher, start, reserve,
                      save, set, send_statistics, start_reg)


async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start.router)
    dp.include_router(start_reg.router)
    dp.include_router(save.router)
    dp.include_router(set.router)
    dp.include_router(register_teacher.router)
    dp.include_router(reserve.router)


    for i in PRESENCE_REPORT:
        ps = i.split(':')
        scheduler.add_job(send_statistics, 'cron', hour=int(ps[0]), minute=int(ps[1]), day_of_week='0-5')
    ps = PRESENCE_REPORT_LOG.split(':')
    scheduler.add_job(send_statistics, 'cron', [True] , hour=int(ps[0]), minute=int(ps[1]), day_of_week='0-5')

    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())