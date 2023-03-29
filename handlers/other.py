from aiogram import types, Dispatcher
from create_bot import dp

#сюда въебем штуку, которая удаляет сообщения с матом
#@dp.message_handler()
async def echo_send(message: types.message):
    pass

def regist_handlers_other(dp: Dispatcher):
    pass