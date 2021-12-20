from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from loader import emojis

get_contact_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
get_contact_menu.insert(KeyboardButton(text=f"{emojis.mobile_phone} Поделиться номером телефона",
                                       request_contact=True))
get_contact_menu.insert(KeyboardButton(text=f"{emojis.cross_mark} Отписаться от получения статусов"))
get_contact_menu.insert(KeyboardButton(text=f"{emojis.home} Главное меню"))
