from json import dumps

from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter, Text
from aiogram.dispatcher.storage import FSMContext

from keyboards.default.cancel import cancel_def_menu
from keyboards.default.get_contact import get_contact_menu
from keyboards.inline.backtotop import backtotopmenu
from keyboards.inline.callback_datas import main_callback, unsubscribe_statuses_callback
from keyboards.inline.main import mainmenu
from keyboards.inline.unsubscribe_statuses import unsubscribemenu
from loader import dispatcher, db_connector, emojis, iis_connector
from states.transfer_personal_data import TransferPersonalDataQuestions


@dispatcher.callback_query_handler(main_callback.filter(main_choice="transmit_surname_and_mobile"))
async def surname_and_mobile_choice(call: types.CallbackQuery):
    tg_user_id = call.from_user.id
    user_info = await db_connector.get_user_info(tg_user_id)
    if not user_info:
        await call.message.delete()
        await call.message.answer(f"{emojis.warning} Сначала выберете район!", reply_markup=backtotopmenu)
    else:
        msg = [
            "Чтобы я смог находить все ваши дела, сообщите мне ваши номер телефона и фамилию.",
            "",
            "Поделитесь номером телефона, нажав на кнопку ниже, в меню, под клавиатурой. Затем я спрошу вашу фамилию.",
            "",
            "Если хотите прекратить получать оповещения в автоматическом режиме, то нажмите соответствующую кнопку "
            "и я удалю ваши данные из базы бота.",
            "",
            f"Если хотите отменить действие, нажмите на кнопку {emojis.home} <b>Главное меню</b>."
        ]
        await call.message.delete()
        await call.message.answer("\n".join(msg), reply_markup=get_contact_menu)
        await TransferPersonalDataQuestions.first()


@dispatcher.message_handler(content_types=types.ContentTypes.CONTACT, state=TransferPersonalDataQuestions.Q1)
async def get_mobile(message: types.Message, state: FSMContext):
    mobile = f"+{message.contact.phone_number.strip('+')}"
    await state.update_data(mobile=mobile)
    await message.answer("Номер телефона получен!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Теперь введите фамилию.", reply_markup=cancel_def_menu)
    await TransferPersonalDataQuestions.next()


@dispatcher.message_handler(Text(f"{emojis.cross_mark} Отмена"), state=TransferPersonalDataQuestions.Q2)
async def cancel_personal_data_entry(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили ввод своих персональных данных.",
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Возвращаемся в главное меню?", reply_markup=backtotopmenu)
    await state.finish()


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=TransferPersonalDataQuestions.Q2)
async def get_surname(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    tg_user_id = message.from_user.id
    surname = message.text
    mobile = state_data.get("mobile")
    # Проверить наличие дел у пользователя.
    # Если дел нет, то не записывать его персональные данные в базу
    user_info = await db_connector.get_user_info(tg_user_id)
    district_id, _, _, _ = user_info[0]
    cases = await iis_connector.get_detail_list_cases(district_id=district_id, surname=surname, mobile=mobile)
    if cases:
        await db_connector.update_user_info(tg_user_id=tg_user_id,
                                            surname=surname,
                                            mobile=mobile,
                                            cases=dumps(cases, ensure_ascii=False))
        msg = [
            "Ваши личные данные собраны и записаны в базу бота, спасибо.",
            "",
            f"Если статус любого вашего дела изменится, то я сообщу вам об этом в автоматическом режиме. {emojis.robot}",
        ]
        await message.answer("\n".join(msg), reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Если вы передумали и хотите отменить оповещения в автоматическом режиме, "
                             "то нажмите на кнопку ниже.", reply_markup=unsubscribemenu)
    else:
        msg = "По вашему номеру телефона и фамилии не нашлось дел!"
        await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Возвращаемся в главное меню?", reply_markup=backtotopmenu)
    await state.finish()


@dispatcher.message_handler(Text(f"{emojis.cross_mark} Отписаться от получения статусов"),
                            state=TransferPersonalDataQuestions.Q1)
async def unsubscribe_statuses(message: types.Message, state: FSMContext):
    tg_user_id = message.from_user.id
    if await db_connector.get_user_info(tg_user_id):
        await db_connector.delete_user(tg_user_id)
        msg = "Вы отменили получение оповещений об изменении статусов дел."
    else:
        msg = "Ваших данных нет в базе бота, нечего удалять."
    await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Возвращаемся в главное меню?", reply_markup=backtotopmenu)
    await state.finish()


@dispatcher.message_handler(Text(f"{emojis.home} Главное меню"), state=TransferPersonalDataQuestions.Q1)
async def backtotop_default_menu(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили ввод своих персональных данных.",
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Добро пожаловать в главное меню, вот что здесь есть:", reply_markup=mainmenu)
    await state.finish()


@dispatcher.callback_query_handler(unsubscribe_statuses_callback.filter(unsubscribe_choice="cancel"))
async def unsubscribe_cancel(call: types.CallbackQuery):
    tg_user_id = call.from_user.id
    if await db_connector.get_user_info(tg_user_id):
        await db_connector.delete_user(tg_user_id)
        await call.answer("Вы отменили получение оповещений об изменении статусов дел.", show_alert=True)
    else:
        await call.answer("Ваших данных нет в базе бота, нечего удалять.", show_alert=True)
    await call.message.edit_text("Добро пожаловать в главное меню, вот что здесь есть:")
    await call.message.edit_reply_markup(reply_markup=mainmenu)
