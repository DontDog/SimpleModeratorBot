from aiogram import Bot
from app.config import TOKEN
from db import UserDatabase

bot = Bot(token=TOKEN)
teachers_db = UserDatabase(filename="teachers_db.csv")