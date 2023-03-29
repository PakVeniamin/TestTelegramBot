from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#Добавим кнопки для админа, чтобы загружать и удалять данные

button_to_load = KeyboardButton('/Загрузить')
button_to_delete = KeyboardButton('/Удалить')

button_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_to_load)\
    .add(button_to_delete)