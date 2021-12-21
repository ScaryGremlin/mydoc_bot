from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.dispatcher.storage import FSMContext

from keyboards.inline.backtotop import backtotopmenu
from keyboards.inline.callback_datas import main_callback
from loader import db_connector
from loader import dispatcher, emojis
from states.feedback import FeedbackQuestions


@dispatcher.callback_query_handler(main_callback.filter(main_choice="feedback"))
async def feedback_main_choice(call: types.CallbackQuery):
    msg = [
        "Если у вас есть жалоба, предложение или отзыв о работе, "
        "поделитесь ими в ответном сообщении.",
        "Если у вас возникла проблема в работе с ботом, то напишите об этом в ЛС разработчику — "
        "@ScaryGremlin",
        "",
        f"{emojis.warning} Для того, чтобы оставить жалобу, предложение или отзыв о работе, необходимо "
        "сообщить свои персональные данные.",
        "Сделать это можно в главном меню.",
    ]
    await call.message.edit_text("\n".join(msg))
    await call.message.edit_reply_markup(reply_markup=backtotopmenu)
    await FeedbackQuestions.first()


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=FeedbackQuestions.Q1)
async def get_feedback(message: types.Message, state: FSMContext):
    tg_user_id = message.from_user.id
    feedback_text = message.text
    user_info = await db_connector.get_user_info(tg_user_id)
    # Если пользователь есть в базе бота и есть его фамилия и телефон,
    # то отправить текст обратной связи
    if user_info and user_info[0][1] and user_info[0][2]:
        _, surname, mobile, _ = user_info[0]
