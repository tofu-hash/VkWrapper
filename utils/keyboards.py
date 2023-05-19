from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

cancel_button = InlineKeyboardButton(text='❌ Отмена',
                                     callback_data='cancel')
cancel = InlineKeyboardMarkup().add(cancel_button)

change_model = InlineKeyboardMarkup()
change_model.add(InlineKeyboardButton(text='text-davinci-003',
                                      callback_data='text-davinci-003'))
change_model.add(InlineKeyboardButton(text='gpt-3.5-turbo',
                                      callback_data='gpt-3.5-turbo'))
change_model.add(cancel_button)

add_openai_api_key = InlineKeyboardMarkup()
add_openai_api_key.add(InlineKeyboardButton(text='Создать ключ',
                                            url='https://vkhost.github.io'))
add_openai_api_key.add(cancel_button)
