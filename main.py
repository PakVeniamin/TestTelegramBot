from aiogram import executor
from create_bot import dp
from database import creator
async def on_startup(_):
    print('Бот в онлайне')
    creator.connection_database()
    creator.connect_update_database()

from handlers import client, admin, other

client.regist_handlers_client(dp)
admin.register_admin_handlers(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
