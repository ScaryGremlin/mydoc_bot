from aiogram import types

from keyboards.inline.backtotop import backtotopmenu
from keyboards.inline.callback_datas import main_callback
from loader import dispatcher, emojis


@dispatcher.callback_query_handler(main_callback.filter(main_choice="help"))
async def main_menu(call: types.CallbackQuery):
    msg = [
        "<b>Что можно сделать с помощью этого бота?</b>",
        "",
        f"{emojis.check_mark} <b>Узнать статус дела.</b> "
        f"Выбрав этот пункт главного меню, можно сообщить боту номер дела и "
        "в ответном сообщении он пришлёт статус по номеру. "
        "Сообщите боту свои ФИО и СНИЛС, чтобы он выбирал Ваши дела и сообщал о статусах автоматически.",
        f"{emojis.check_mark} <b>Посмотреть список всех наших отделений.</b> "
        "Здесь можно посмотреть детальную информацию по каждому из отделений.",
        f"{emojis.check_mark} <b>Найти два ближайших к Вам отделения.</b> "
        "Бот покажет два отделения, которые находятся ближе всего к Вам по дороге, учитывая график работы — "
        "те отделения, которые в данный момент закрыты, показаны не будут.",
        f"{emojis.check_mark} <b>Оставить обратную связь.</b> "
        "Если Вы хотите оставить отзыв, жалобу или у Вас есть замечания по работе бота, "
        "можете воспользоваться этим пунктом меню.",
    ]
    await call.message.edit_text("\n".join(msg))
    await call.message.edit_reply_markup(reply_markup=backtotopmenu)
