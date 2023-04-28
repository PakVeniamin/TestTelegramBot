from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from database.creator import return_data, del_data, full_table_stsrategy
from keyboards import admin_buttons
from create_bot import dp, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


#https://iss.moex.com/iss/engines/futures/markets/options/boards/ROPD/securities.json  options
myID = 690148599

class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    recomendation = State()

#@.dp.message_handler(commands=['admin'], is_chat_admin = True)
async def make_changes(message: types.Message):
    if (message.from_user.id == myID):
        await bot.send_message(message.from_user.id, 'Админ привет, че хотел?', reply_markup=admin_buttons.button_admin)
    else:
        await message.reply('Вы не админ')

#@dp.message_handler(commands='Загрузить', state=None)
async def strategy(message: types.Message):
    if (message.from_user.id == myID):
        await FSMadmin.photo.set()
        await message.reply("Загрузите фото")
    else:
        await message.reply('Вы не админ')


#@dp.message_handler(content_types=["photo"], state=FSMadmin.photo)
async def loading_photo(message:types.Message, state=FSMContext):
    async with state.proxy() as proxy:
        proxy["photo"] = message.photo[0].file_id
    await FSMadmin.next()
    await message.reply("Придумайте название")

#@dp.message_handler(state=FSMadmin.name)
async def enter_name(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['name'] = message.text
    await FSMadmin.next()
    await message.reply('Введите описание')


#@dp.message_handler(state=FSMadmin.description)
async def enter_description(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['description'] = message.text
    await FSMadmin.next()
    await message.reply('Какие будут рекомендации?')

#@dp.message_handler(state=FSMadmin.recomendation)
async def enter_recomendation(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['recomendation'] = message.text

    await full_table_stsrategy(state)
    await state.finish()

#@dp.callback_query_handlers(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await del_data(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)

#@dp.message_handlers(commands = 'Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == myID:
        read = await return_data()
        for i in read:
            await bot.send_photo(message.from_user.id, i[0], f'{i[1]}\nОписание: {i[2]}\nЦена {i[-1]}')
            await bot.send_message(message.from_user.id, text='^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Удалить {i[1]}', callback_data=f'del {i[1]}')))
    else:
        await message.reply("Вы не админ")
#Регистрация хендлеров
def register_admin_handlers(dp:Dispatcher):
    dp.register_message_handler(strategy, commands='Загрузить', state=None)
    dp.register_message_handler(loading_photo, content_types=["photo"], state=FSMadmin.photo)
    dp.register_message_handler(enter_name, state=FSMadmin.name)
    dp.register_message_handler(enter_description,state=FSMadmin.description)
    dp.register_message_handler(enter_recomendation, state=FSMadmin.recomendation)
    dp.register_message_handler(make_changes, commands='moder')
    dp.register_message_handler(delete_item, commands='Удалить')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))