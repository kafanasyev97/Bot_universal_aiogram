from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv
load_dotenv()


storage = MemoryStorage()
bot = Bot(token= os.getenv('BOT_TOKEN'))
API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')
API_KEY_CONVERT = os.getenv('API_KEY_CONVERT')
dp = Dispatcher(bot, storage=storage)
