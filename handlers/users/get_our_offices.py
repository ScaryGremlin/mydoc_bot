from itertools import islice

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters import ViaBot
from keyboards.inline.backtotop import backtotopmenu
from keyboards.inline.callback_datas import office_callback
from loader import dispatcher, emojis, iis_connector, bot_id, urls, db_connector


@dispatcher.inline_handler(text="offices")
async def select_our_office_command(query: types.InlineQuery):
    tg_user_id = query.from_user.id
    offset = int(query.offset) if query.offset else 0
    user_info = await db_connector.get_user_info(tg_user_id)
    results_inline_query = []
    if user_info:
        district_id, _, _, _ = user_info[0]
        all_our_offices = await iis_connector.get_subdivisions_list(district_id)
        choice_office_text = "<b>Выбран офис: </b>"
        for subdivision in islice(all_our_offices, offset, offset + 50):
            subdivision_small_name = f"{subdivision.get('naz_s')}"
            results_inline_query.append(types.InlineQueryResultArticle(
                id=subdivision.get("ids"),
                title=subdivision.get("naz_s"),
                input_message_content=types.InputTextMessageContent(
                    message_text=f"{choice_office_text}{subdivision_small_name}"
                ),
                description=subdivision.get("adr")
            ))
        if len(results_inline_query) < 50:
            # Результатов больше не будет, next_offset пустой
            await query.answer(results_inline_query, is_personal=True, next_offset=None, cache_time=0)
        else:
            # Ожидаем следующую порцию данных
            await query.answer(results_inline_query, is_personal=True, next_offset=str(offset + 50), cache_time=0)
        await query.answer(results_inline_query, cache_time=0)
    # Если пользователя нет в базе, то сообщить о необходимости указать район
    else:
        description = [
            "Сначала сообщите боту интересующий вас район.",
            "Выберете в главном меню соответствующий пункт.",
        ]
        message_text = "<code>Не выбран район</code>"
        results_inline_query.append(types.InlineQueryResultArticle(
            id="None",
            title=f"{emojis.warning} Не выбран район.",
            input_message_content=types.InputTextMessageContent(message_text=message_text),
            description="\n".join(description)
        ))
        await query.answer(results_inline_query, cache_time=0)


@dispatcher.message_handler(Text(startswith="Выбран офис: "), ViaBot(bot_id))
async def get_detail_office(message: types.Message):
    subdivision_small_name = message.text[13:]
    subdivision_detail = iis_connector.get_subdivision_detail(subdivision_small_name)
    if subdivision_detail:
        officemenu = InlineKeyboardMarkup(row_width=1)
        officemenu.insert(InlineKeyboardButton(text=f"{emojis.five_o_clock} Расписание в подразделении",
                                               callback_data=office_callback.new(office_choice="subdivision_schedule",
                                                                                 office_id=subdivision_detail.get("ids")
                                                                                 )))
        if isinstance(subdivision_detail.get("map"), dict):
            google_maps_url = urls.google_maps.format(lat=subdivision_detail.get("map").get("x"),
                                                      lon=subdivision_detail.get("map").get("y"))

            officemenu.insert(InlineKeyboardButton(text=f"{emojis.world_map} Показать на карте google",
                                                   callback_data=office_callback.new(office_choice="google_maps",
                                                                                     office_id="None"),
                                                   url=google_maps_url))

        officemenu.insert(InlineKeyboardButton(text=f"{emojis.home} Главное меню",
                                               callback_data=office_callback.new(office_choice="backtotop",
                                                                                 office_id="None"
                                                                                 )))
        msg = [
            f"<b>Полное наименование:</b> <code>{subdivision_detail.get('naz')}</code>",
            f"<b>Адрес:</b> <code>{subdivision_detail.get('adr')}</code>",
            f"<b>Почта:</b> <code>{subdivision_detail.get('email')}</code>",
            f"<b>Телефон:</b> <code>{subdivision_detail.get('tel')}</code>",
        ]
        await message.answer("\n".join(msg), reply_markup=officemenu)
    else:
        msg = [
            f"{emojis.warning} Нет данных по подразделению в базе данных МФЦ",
        ]
        await message.answer("\n".join(msg), reply_markup=backtotopmenu)


@dispatcher.callback_query_handler(office_callback.filter(office_choice="subdivision_schedule"))
async def show_subdivision_schedule(call: types.CallbackQuery, callback_data: dict):
    tg_user_id = call.from_user.id
    user_info = await db_connector.get_user_info(tg_user_id)
    district_id, _, _, _ = user_info[0]
    schedule_subdivision = await iis_connector.get_subdivision_schedule(district_id, callback_data.get("office_id"))
    await call.message.edit_text(f"<code>{schedule_subdivision}</code>")
    await call.message.edit_reply_markup(reply_markup=backtotopmenu)
