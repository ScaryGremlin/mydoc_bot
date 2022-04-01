from aiogram import types

from loader import dispatcher
# from loader import iis_connector
from keyboards.inline.callback_datas import main_callback
from keyboards.inline.backtotop import backtotopmenu


# @dispatcher.inline_handler(text="near")
# async def near_offices_choice(query: types.InlineQuery):
@dispatcher.callback_query_handler(main_callback.filter(main_choice="near"))
async def near_offices_choice(call: types.CallbackQuery):
    # Узнать текущие координаты пользователя и передать их
    # в функцию нахождения двух ближайших офисов

    # lat = query.location.latitude
    # lon = query.location.longitude
    # results_inline_menu = []
    # for near_subdivision in iis_connector.get_near_offices(lat, lon, number_nearest=2):
    #     subdivision_address = near_subdivision.get("adr")
    #     distance = near_subdivision.get("distance") / 1000
    #     duration = near_subdivision.get("duration")
    #     description = [
    #         f"{subdivision_address}",
    #         f"Расстояние: {distance}",
    #         f"Время в пути: {duration}",
    #     ]
    #     results_inline_menu.append(types.InlineQueryResultArticle(
    #         id=near_subdivision.get("ids"),
    #         title=near_subdivision.get("naz_s"),
    #         input_message_content=types.InputMessageContent(message_text=near_subdivision.get("naz_s")),
    #         description="\n".join(description)
    #     ))
    # await query.answer(results_inline_menu, is_personal=True, cache_time=0)
    msg = [
        "Извините, раздел находится в разработке. Скоро должен заработать.",
    ]
    await call.answer()
    await call.message.edit_text("\n".join(msg))
    await call.message.edit_reply_markup(reply_markup=backtotopmenu)
