from aiogram.utils.callback_data import CallbackData

main_callback = CallbackData("mainmenu", "main_choice")
transfer_data_callback = CallbackData("transferdatamenu", "transferdata_choice")
case_callback = CallbackData("casemenu", "case_choice")
office_callback = CallbackData("officemenu", "office_choice", "office_id")
near_offices_callback = CallbackData("nearofficesmenu", "nearoffices_choice")
backtotop_callback = CallbackData("backtotopmenu", "backtotop_choice")
cancel_callback = CallbackData("cancelmenu", "cancel_choice")
unsubscribe_statuses_callback = CallbackData("unsubscribemenu", "unsubscribe_choice")
