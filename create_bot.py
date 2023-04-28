from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token="5902309415:AAESFf9GX5nTP2kbTHBzb6hXsNSKoVnqKak")
dp = Dispatcher(bot, storage=storage)