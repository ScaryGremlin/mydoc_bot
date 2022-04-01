import mimetypes
import smtplib
from email.message import EmailMessage
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


def send_mail(sender: str, recipients: list, subject: str, body: str, creds: dict, attachment: str = None):
    """
    Отправить сообщение электронной почты
    :param sender: Отправитель письма
    :param recipients: Список получателей письма
    :param subject: Тема письма
    :param body: Тело письма
    :param attachment: Файл для отправки
    :param creds:
    """
    email_message = EmailMessage()
    email_message["Subject"] = subject
    email_message["To"] = recipients
    email_message["From"] = sender
    email_message.preamble = "You will not see this in a MIME-aware mail reader. \n"
    if attachment:
        ctype, encoding = mimetypes.guess_type(attachment)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(attachment, 'rb') as attached_file:
            email_message.add_attachment(attached_file.read(), maintype=maintype,
                                         subtype=subtype, filename=attachment)
    email_message.set_content(body)
    smtp_server = creds.get("smtp").get("server")
    smtp_port = creds.get("smtp").get("port")
    smtp_login = creds.get("login")
    smtp_password = creds.get("password")
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp_conn:
        smtp_conn.login(smtp_login, smtp_password)
        smtp_conn.send_message(email_message)
