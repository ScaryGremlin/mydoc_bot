from itertools import islice

from aiogram import types
from aiogram.dispatcher.filters import Text

from filters import ViaBot
from keyboards.inline.backtotop import backtotopmenu
from loader import dispatcher, emojis, bot_id, db_connector, districts
from utils.misc import get_dict_key


@dispatcher.inline_handler(text="districts")
async def select_district_command(query: types.InlineQuery):
    offset = int(query.offset) if query.offset else 0
    results_inline_query = []
    choice_district_text = "<b>Выбран район: </b>"
    for district in islice(districts.items(), offset, offset + 50):
        office_number, district_name = district
        results_inline_query.append(types.InlineQueryResultArticle(
            id=office_number,
            title=district_name,
            input_message_content=types.InputTextMessageContent(message_text=f"{choice_district_text}{district_name}"),
            description=district_name
        ))
    if len(results_inline_query) < 50:
        # Результатов больше не будет, next_offset пустой
        await query.answer(results_inline_query, is_personal=True, next_offset=None, cache_time=0)
    else:
        # Ожидаем следующую порцию данных
        await query.answer(results_inline_query, is_personal=True, next_offset=str(offset + 50), cache_time=0)
    await query.answer(results_inline_query, cache_time=0)


@dispatcher.message_handler(Text(startswith="Выбран район:"), ViaBot(bot_id))
async def set_user_district(message: types.Message):
    tg_user_id = message.from_user.id
    # Удалить текст "Выбран район: "
    district_name = message.text[14:]
    district_id = get_dict_key(districts, district_name)
    await db_connector.add_or_replace_user(tg_user_id=tg_user_id, district_id=district_id)
    msg = [
        f"{emojis.warning} Внимание!",
        "",
        "После выбора района необходимо заново сообщить боту номер телефона и фамилию.",
        "",
        "Сделать это можно выбрав соответствующий пункт в главном меню.",
    ]
    await message.answer("\n".join(msg), reply_markup=backtotopmenu)
