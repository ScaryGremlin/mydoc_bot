from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import transfer_data_callback
from keyboards.inline.callback_datas import cancel_callback
from loader import emojis

transferdatamenu = InlineKeyboardMarkup(row_width=1)
transferdatamenu.insert(InlineKeyboardButton(text="Удалить ФИО и СНИЛС из базы бота",
                                             callback_data=transfer_data_callback.new(transferdata_choice="delete_data")))
transferdatamenu.insert(InlineKeyboardButton(text=f"{emojis.cross_mark} Отмена",
                                             callback_data=cancel_callback.new(cancel_choice="cancel")))
