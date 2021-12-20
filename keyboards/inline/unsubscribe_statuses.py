from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import unsubscribe_statuses_callback
from loader import emojis

unsubscribemenu = InlineKeyboardMarkup(row_width=1)
unsubscribemenu.insert(InlineKeyboardButton(text=f"{emojis.cross_mark} Отписаться от получения статусов",
                                            callback_data=unsubscribe_statuses_callback.new(unsubscribe_choice="cancel")))
unsubscribemenu.insert(InlineKeyboardButton(text=f"{emojis.home} Главное меню",
                                            callback_data=unsubscribe_statuses_callback.new(unsubscribe_choice="backtotop")))
