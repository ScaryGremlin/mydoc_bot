from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import near_offices_callback
from loader import emojis

locationmenu = InlineKeyboardMarkup(row_width=1)
locationmenu.insert(InlineKeyboardButton(text=f"{emojis.round_pushpin}",
                                         callback_data=near_offices_callback.new(nearoffices_choice="get_location"),
                                         request_location=True))
locationmenu.insert(InlineKeyboardButton(text=f"{emojis.home} Главное меню",
                                         callback_data=near_offices_callback.new(nearoffices_choice="backtotop")))
