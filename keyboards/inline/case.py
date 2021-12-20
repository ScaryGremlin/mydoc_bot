from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import case_callback
from loader import emojis

casemenu = InlineKeyboardMarkup(row_width=1)
casemenu.insert(InlineKeyboardButton(text="По номеру дела",
                                     callback_data=case_callback.new(case_choice="stat_by_num")))
casemenu.insert(InlineKeyboardButton(text="По фамилии и номеру телефона",
                                     switch_inline_query_current_chat="cases"))
casemenu.insert(InlineKeyboardButton(text=f"{emojis.home} Главное меню",
                                     callback_data=case_callback.new(case_choice="backtotop")))
