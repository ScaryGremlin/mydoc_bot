from itertools import islice
from json import loads

from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter, Text
from aiogram.dispatcher.storage import FSMContext

from filters import ViaBot
from keyboards.inline.backtotop import backtotopmenu
from keyboards.inline.callback_datas import main_callback, case_callback
from keyboards.inline.cancel import cancelmenu
from keyboards.inline.case import casemenu
from loader import dispatcher, emojis, iis_connector, bot_id, db_connector
from states.case_status import CaseStatusQuestions
from utils import misc


@dispatcher.callback_query_handler(main_callback.filter(main_choice="case_status"))
async def case_status_choice(call: types.CallbackQuery):
    msg = [
        f"Хорошо, уточните, пожалуйста, как бы вы хотели узнать статус дела? {emojis.thinking_face}",
    ]
    await call.message.edit_text("\n".join(msg))
    await call.message.edit_reply_markup(reply_markup=casemenu)


@dispatcher.callback_query_handler(case_callback.filter(case_choice="stat_by_num"))
async def get_case_status_by_num(call: types.CallbackQuery):
    msg = [
        "Сообщите мне номер дела в формате: <code>21_01-123456</code>",
        "Этот номер указан на вашей расписке.",
        "Пожалуйста, будте внимательны к символам подчёркивания и тире!",
        "Не допускайте ввода пробелов!",
    ]
    await call.message.edit_text("\n".join(msg))
    await call.message.edit_reply_markup(reply_markup=cancelmenu)
    await CaseStatusQuestions.first()


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=CaseStatusQuestions.Q1)
async def get_case_info_by_num(message: types.Message, state: FSMContext):
    tg_user_id = message.from_user.id
    case_number = message.text
    user_info = await db_connector.get_user_info(tg_user_id)
    if user_info:
        district_id, _, _, _ = user_info[0]
        case_status = await iis_connector.get_case_status(district_id, case_number)
        await message.answer(f"{case_status}")
    else:
        msg = [
            f"{emojis.warning} Сначала выберете район!",
            "Сделать это можно в главном меню"
        ]
        await message.answer("\n".join(msg))
    await message.answer(f"Хорошо, уточните, пожалуйста, как бы вы хотели узнать статус дела? "
                         f"{emojis.thinking_face}", reply_markup=casemenu)
    await state.finish()


@dispatcher.inline_handler(text="cases")
async def get_case_status_by_personal_data(query: types.InlineQuery):
    tg_user_id = query.from_user.id
    offset = int(query.offset) if query.offset else 0
    user_info = await db_connector.get_user_info(tg_user_id)
    results_inline_query = []
    # Если пользователь есть в базе бота и есть его дела
    if user_info and user_info[0][3]:
        _, surname, mobile, cases_as_string = user_info[0]
        cases = loads(cases_as_string)
        choice_case_text = "<b>Выбрано дело: </b>"
        for case in islice(cases.get("data"), offset, offset + 50):
            description = misc.get_description(case.get("status").capitalize())
            case_number_text = f"<code>{case.get('delonum')}</code>"
            results_inline_query.append(types.InlineQueryResultArticle(
                id=case.get("delonum"),
                title=f"{emojis.clipboard} Дело № {case.get('delonum')}",
                input_message_content=types.InputTextMessageContent(message_text=f"{choice_case_text}{case_number_text}"),
                description="\n".join(description)
            ))
        if len(results_inline_query) < 50:
            # Результатов больше не будет, next_offset пустой
            await query.answer(results_inline_query, is_personal=True, next_offset=None, cache_time=0)
        else:
            # Ожидаем следующую порцию данных
            await query.answer(results_inline_query, is_personal=True, next_offset=str(offset + 50), cache_time=0)
        await query.answer(results_inline_query, cache_time=0)
    # Если пользователя нет в базе, то сообщить о необходимости внести персональные данные
    else:
        description = [
            "Сначала сообщите боту свои персональные данные — номер телефона и фамилию.",
            "Выберете в главноем меню соответствующий пункт.",
        ]
        message_text = "<code>Нет персональных данных</code>"
        results_inline_query.append(types.InlineQueryResultArticle(
                id="None",
                title=f"{emojis.warning} Нет персональных данных.",
                input_message_content=types.InputTextMessageContent(message_text=message_text),
                description="\n".join(description)
            ))
        await query.answer(results_inline_query, cache_time=0)


@dispatcher.message_handler(Text(startswith="Выбрано дело: "), ViaBot(bot_id))
async def get_detail_case_by_personal_data(message: types.Message):
    tg_user_id = message.from_user.id
    case_number = message.text[14:]
    user_info = await db_connector.get_user_info(tg_user_id)
    if user_info:
        _, _, _, cases_as_string = user_info[0]
        cases = loads(cases_as_string)
        msg = next((case for case in cases.get("data") if case.get("delonum") == case_number), None)
        await message.answer(f"<code>{msg}</code>", reply_markup=backtotopmenu)
