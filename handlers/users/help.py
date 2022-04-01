from aiogram import types

from keyboards.inline.backtotop import backtotopmenu
from keyboards.inline.callback_datas import main_callback
from loader import dispatcher, emojis


@dispatcher.callback_query_handler(main_callback.filter(main_choice="help"))
async def get_help(call: types.CallbackQuery):
    msg = [
        "<b>Что можно сделать с помощью этого бота?</b>",
        "",
        f"{emojis.check_mark} <b>Узнать статус дела.</b> "
        f"Выбрав этот пункт главного меню, можно сообщить боту номер дела и "
        "в ответном сообщении он пришлёт статус по номеру. "
        "Сообщите боту свои номер телефона и фамилию, чтобы он выбирал ваши дела и сообщал о статусах автоматически.",
        f"{emojis.check_mark} <b>Посмотреть список всех наших отделений.</b> "
        "Здесь можно посмотреть детальную информацию по каждому из отделений.",
        f"{emojis.check_mark} <b>Найти два ближайших к вам отделения.</b> "
        "Бот покажет два отделения, которые находятся ближе всего к вам по дороге.",
        f"{emojis.check_mark} <b>Обратная связь.</b> "
        "Если вы хотите оставить отзыв или жалобу о работе наших отделений, можете воспользоваться этим пунктом меню.",
        "",
        "Если что-то пошло не так в работе бота и вы не понимаете, как такое возможно, "
        "свяжитесь с @arthur_dzhemakulov.",
    ]
    await call.message.edit_text("\n".join(msg))
    await call.message.edit_reply_markup(reply_markup=backtotopmenu)
