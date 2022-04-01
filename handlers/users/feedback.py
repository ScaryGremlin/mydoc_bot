from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.dispatcher.storage import FSMContext

from data import creds
from keyboards.inline.backtotop import backtotopmenu
from keyboards.inline.callback_datas import main_callback
from keyboards.inline.cancel import cancelmenu
from keyboards.inline.main import mainmenu
from loader import db_connector
from loader import dispatcher, emojis
from states.feedback import FeedbackQuestions
from utils import misc


@dispatcher.callback_query_handler(main_callback.filter(main_choice="feedback"))
async def feedback_main_choice(call: types.CallbackQuery, state: FSMContext):
    tg_user_id = call.from_user.id
    user_info = await db_connector.get_user_info(tg_user_id)
    # Если пользователь есть в базе бота, то отправить текст обратной связи
    if user_info:
        msg = [
            f"{emojis.slightly_smiling_face} {emojis.frowning_face} "
            "Если у вас есть жалоба, предложение или отзыв о работе наших офисов, поделитесь ими в ответном сообщении.",
        ]
        await call.message.edit_text("\n".join(msg))
        await call.message.edit_reply_markup(reply_markup=cancelmenu)
        await FeedbackQuestions.first()
        _, surname, mobile, _ = user_info[0]
        await state.update_data(mobile=mobile, surname=surname)
    else:
        msg = [
            f"{emojis.warning} Для того, чтобы оставить жалобу, предложение или отзыв о работе, необходимо "
            "сообщить свои персональные данные.",
            "Сделать это можно в главном меню.",
        ]
        await call.answer()
        await call.message.edit_text("\n".join(msg))
        await call.message.edit_reply_markup(reply_markup=backtotopmenu)


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=FeedbackQuestions.Q1)
async def get_feedback(message: types.Message, state: FSMContext):
    # Отправить почту с текстом отзыва
    sender = creds.SMTP_LOGIN
    recipients = creds.RECIPIENTS_EMAIL
    subject = "From telegram bot feedback"
    state_data = await state.get_data()
    mobile = state_data.get('mobile')
    surname = state_data.get('surname')
    body = [
        message.text,
        f"Мобильный телефон: {mobile}",
        f"ФИО: {surname}",
    ]
    mail_creds = {
        "smtp": {
            "server": creds.SMTP_SERVER,
            "port": creds.SMTP_PORT,
        },
        "login": creds.SMTP_LOGIN,
        "password": creds.SMTP_PASS,
    }
    misc.send_mail(sender=sender, recipients=recipients, subject=subject,
                   body="\n".join(body), creds=mail_creds)
    await state.finish()
    msg = [
        "Спасибо за обратную связь. "
        "Ваше сообщение будет доставлено нам на электронную почту. "
        "Мы непременно с вами свяжемся!",
    ]
    await message.answer("\n".join(msg))
    await message.answer("Добро пожаловать в главное меню, вот что здесь есть:",
                         reply_markup=mainmenu)
