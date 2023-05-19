from aiogram.bot import Bot
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, BotCommand, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_middleware import *
from utils import states, keyboards

import logging

import config

logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="w")

bot = Bot(token=config.API_KEY)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
