from typing import Union

from loader import emojis


def get_personal_data_from_string(raw_string: str) -> Union[tuple, None]:
    """
    Получить персональные данные - фамилию, имя, отчество и СНИЛС из сырой строки.
    :param raw_string: Строка сырых данных
    :return: Кортеж с фамилией, именем, отчеством и СНИЛСом.
    """
    try:
        fio, raw_snils = raw_string.split(",")
    except ValueError:
        return None
    try:
        surname, name, middlename = fio.split()
    except ValueError:
        return None
    snils = raw_snils.strip().replace("-", "").replace(" ", "")
    return (
        surname.capitalize(),
        name.capitalize(),
        middlename.capitalize(),
        f"{snils[:3]}-{snils[3:6]}-{snils[6:9]} {snils[9:]}"
    )


def get_description(status_info: str, status_exec: str = "") -> list:
    """

    :param status_info:
    :param status_exec:
    :return:
    """
    if status_info.lower() == "исполнено":
        return [f"{emojis.check_mark} {status_info}", status_exec]
    elif status_info.lower() == "отказ":
        return [f"{emojis.cross_mark} {status_info}", status_exec]
    elif status_info.lower() == "в работе":
        return [f"{emojis.technologist} {status_info}", status_exec]
    elif status_info.lower() == "приостановлено":
        return [f"{emojis.stop_sign} {status_info}", status_exec]
    return []


def compare_lists(list_cases_from_db: list, list_cases_from_iis: list) -> list:
    """
    Сравнить два списка. Возвращает пустой список, если сравниваемые
    списки одинаковые и список с различными элементами в противном случае
    :param list_cases_from_db: Первый список
    :param list_cases_from_iis: Второй список
    :return: Список с результатом сравнений
    """
    return [case for case in list_cases_from_iis if case not in list_cases_from_db]


def get_dict_key(some_dict: dict, search_value: str) -> str:
    """

    :param some_dict:
    :param search_value:
    :return:
    """
    for key, value in some_dict.items():
        if value == search_value:
            return key


def get_change_case_status_msg(raw_data: list) -> list:
    """

    :param raw_data:
    :return:
    """
    msg = [
        "<b>Изменения статусов ваших дел:</b>",
        "",
    ]
    for case in raw_data:
        msg.append(f"<b>Номер дела: </b><code>{case.get('delonum')}</code>")
        msg.append(f"<b>Услуга: </b><code>{case.get('nusl')}</code>")
        msg.append(f"<b>Статус: </b><code>{case.get('status')}, {case.get('status_detail')}</code>")
        msg.append("")
    return msg
