from json import dumps, loads
from operator import itemgetter

from aiogram import Dispatcher

from loader import iis_connector, db_connector
from utils import misc


async def check_cases_statuses(dispatcher: Dispatcher):
    """

    :param dispatcher:
    :return:
    """
    # Получить текущие данные всех пользователей из базы данных бота
    users_info = await db_connector.select_all_users()
    for user_info in users_info:
        tg_user_id, district_id, surname, mobile, cases_from_bot_as_string = user_info
        if cases_from_bot_as_string:
            # Получить статусы дел из базы данных бота по текущему пользователю
            cases_from_bot = loads(cases_from_bot_as_string)
            list_cases_from_bot_db = sorted(cases_from_bot.get("data"), key=itemgetter("id"))
            # Получить статусы дел из информационной системы по текущему пользователю
            cases_from_iis = await iis_connector.get_detail_list_cases(district_id=district_id,
                                                                       surname=surname,
                                                                       mobile=mobile)
            list_cases_from_iis = sorted(cases_from_iis.get("data"), key=itemgetter("id"))
            # Сравнить два словаря - словарь с текущими статусами из базы бота
            # и словарь из дел со статусами из информационной системы.
            # Если есть различия то вернуть словарь с различиями -
            # изменившимися статусами дел и записать новые статусы в базу данных бота.
            diff_cases = misc.compare_lists(list_cases_from_bot_db, list_cases_from_iis)
            if diff_cases:
                # Сформировать текст сообщения с изменившимися статусами
                msg = misc.get_change_case_status_msg(diff_cases)
                await dispatcher.bot.send_message(chat_id=tg_user_id, text="\n".join(msg))
                # Записать новые статусы в базу бота
                await db_connector.add_or_replace_user(tg_user_id=tg_user_id,
                                                       district_id=district_id,
                                                       surname=surname,
                                                       mobile=mobile,
                                                       cases=dumps(cases_from_iis, ensure_ascii=False))
