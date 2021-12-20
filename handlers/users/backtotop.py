from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from keyboards.inline.callback_datas import (
    case_callback,
    cancel_callback,
    backtotop_callback,
    transfer_data_callback,
    office_callback,
    near_offices_callback,
    unsubscribe_statuses_callback,
)
from keyboards.inline.main import mainmenu
from loader import dispatcher
from states.case_status import CaseStatusQuestions
from states.transfer_personal_data import TransferPersonalDataQuestions


@dispatcher.callback_query_handler(near_offices_callback.filter(nearoffices_choice="backtotop"))
@dispatcher.callback_query_handler(office_callback.filter(office_choice="backtotop"))
@dispatcher.callback_query_handler(transfer_data_callback.filter(transferdata_choice="backtotop"))
@dispatcher.callback_query_handler(case_callback.filter(case_choice="backtotop"))
@dispatcher.callback_query_handler(cancel_callback.filter(cancel_choice="cancel"))
@dispatcher.callback_query_handler(backtotop_callback.filter(backtotop_choice="backtotop"))
@dispatcher.callback_query_handler(unsubscribe_statuses_callback.filter(unsubscribe_choice="backtotop"))
@dispatcher.callback_query_handler(state=CaseStatusQuestions.Q1)
@dispatcher.callback_query_handler(state=TransferPersonalDataQuestions.Q1)
@dispatcher.callback_query_handler(state=TransferPersonalDataQuestions.Q2)
async def backtotop(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text("Добро пожаловать в главное меню, вот что здесь есть:")
    await call.message.edit_reply_markup(reply_markup=mainmenu)
    await state.finish()
