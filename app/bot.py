from aiogram import Bot
from app.config import TOKEN
from db import UserDatabase, ScheduleDatabase
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token=TOKEN)
teachers_db = UserDatabase(filename="teachers_db.csv")
schedule_db = ScheduleDatabase(filename="schedule_db.csv")
scheduler = AsyncIOScheduler()