import asyncio
from aiogram import Dispatcher
from app.bot import bot
from handlers import register


def main():
    dp = Dispatcher()
    dp.include_router(register.router)

    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()