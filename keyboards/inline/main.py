from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import main_callback
from loader import emojis

mainmenu = InlineKeyboardMarkup(row_width=1)
mainmenu.insert(InlineKeyboardButton(text=f"{emojis.world_map} Выбрать район",
                                     switch_inline_query_current_chat="districts"))
mainmenu.insert(InlineKeyboardButton(text=f"{emojis.card_index_dividers} Сообщить фамилию и номер телефона",
                                     callback_data=main_callback.new(main_choice="transmit_surname_and_mobile")))
mainmenu.insert(InlineKeyboardButton(text=f"{emojis.clipboard} Узнать статус дела",
                                     callback_data=main_callback.new(main_choice="case_status")))
mainmenu.insert(InlineKeyboardButton(text=f"{emojis.office_building} Наши отделения",
                                     switch_inline_query_current_chat="offices"))

# mainmenu.insert(InlineKeyboardButton(text=f"{emojis.round_pushpin} Найти два ближайших офиса",
#                                      switch_inline_query_current_chat="near"))

mainmenu.insert(InlineKeyboardButton(text=f"{emojis.round_pushpin} Найти два ближайших офиса",
                                     callback_data=main_callback.new(main_choice="near")))

mainmenu.insert(InlineKeyboardButton(text=f"{emojis.slightly_smiling_face} {emojis.frowning_face} Обратная связь",
                                     callback_data=main_callback.new(main_choice="feedback")))
mainmenu.insert(InlineKeyboardButton(text=f"{emojis.red_question_mark} Помощь",
                                     callback_data=main_callback.new(main_choice="help")))
