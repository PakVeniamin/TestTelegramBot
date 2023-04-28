from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client
from database import creator

#@dp.message_handler(commands=['start'])
async def command_start(message: types.message):
    await bot.send_message(message.from_user.id, "Приветствую!", reply_markup=kb_client)

#@dp.message_handler(commands=['Стратегии'])
async def descriptions_straregy(message: types.Message):
    await creator.sql_bring_out(message)

#@dp.message_handler(commands=['Опционы'])
async def list_of_options(message: types.Message):
    await creator.output_data(message)

def regist_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(descriptions_straregy, commands=['Стратегии'])
    dp.register_message_handler(list_of_options, commands=['Опционы'])