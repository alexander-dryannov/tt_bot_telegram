from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from os import getenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)