from collections import namedtuple
from operator import itemgetter
from typing import Union

import aiohttp
from googlemaps import Client

from data.emojis import Emoji
from data.urls import Urls
from logger import logger


class IisConnector:
    """
    Класс взаимодействия с ИИС
    """
    Response = namedtuple("Response", ["status", "data"])
    __days_of_week = {
        "Понедельник": "Пн",
        "Вторник": "Вт",
        "Среда": "Ср",
        "Четверг": "Чт",
        "Пятница": "Пт",
        "Суббота": "Сб",
        "Воскресенье": "Вс",
    }

    def __init__(self, auth_user: str, auth_pass: str, google_api_client: Client):
        """
        Конструктор
        :param auth_user: http-логин
        :param auth_pass: http-пароль
        """
        self.__http_session = aiohttp.ClientSession()
        self.__auth = aiohttp.BasicAuth(login=auth_user, password=auth_pass)
        self.__gmaps = google_api_client
        self.__subdivisions_list = []
        self.__subdivision_schedule = {}
        self.__emojis = Emoji()
        self.__urls = Urls()

    async def __api_request(self, method: str, url: str, params: dict = None, headers: dict = None) -> Response:
        """

        """
        if method == "get":
            async with self.__http_session.get(url, params=params, auth=self.__auth) as response:
                return self.Response(response.status, await response.json())
        elif method == "post":
            async with self.__http_session.post(url, data=params, headers=headers, auth=self.__auth) as response:
                return self.Response(response.status, await response.json())

    async def get_case_status(self, district_id: str, case_number: str) -> str:
        """
        Возвращает статус дела по его номеру
        :param district_id: id района
        :param case_number: Номер дела
        :return: Строка статуса для вывода пользователю
        """
        url = f"{self.__urls.iis_api_base.format(district_id)}{self.__urls.iis_api_case_status}"
        payload = {"case": case_number}
        response = await self.__api_request(method="get", url=url, params=payload)
        if response.status == 200:
            if "error" in response.data.get("response"):
                msg = [
                    f"{self.__emojis.cross_mark} Дела с таким номером не существует. "
                    f"Проверьте, пожалуйста, корректность ввода номера дела.",
                    f"Обратите внимание на символы подчёркивания и тире!",
                    f"Возможно вы где-то ввели пробел!",
                ]
                return "\n".join(msg)
            else:
                description = response.data.get("response").get("statusExec").get("info") or ""
                return f"""{response.data.get('response').get("statusInfo")}\n{description}"""
        else:
            msg = [
                f"{self.__emojis.cross_mark} Мне не удалось заглянуть в базу.",
                f"<code>Error code: {response.status}</code>"
            ]
            return "\n".join(msg)

    async def get_detail_list_cases(self, district_id: str,
                              surname: str, snils: str = None,
                              mobile: str = None) -> Union[dict, None]:
        """
        Возвращает словарь с делами заявителя по СНИЛС и фамилии
        :param district_id: id района
        :param surname: Фамилия
        :param snils: СНИЛС
        :param mobile: Мобильный телефон
        :return: Словарь дел заявителя
        """
        payload = {
            "fam": surname,
            "cnils": snils,
            "phone": mobile,
        }
        url = f"{self.__urls.iis_api_base.format(district_id)}{self.__urls.iis_api_cases_list}"
        response = await self.__api_request(method="get", url=url, params=payload)
        if response.status == 200:
            if response.data.get("response").get("data"):
                return response.data.get("response")

    async def get_subdivisions_list(self, district_id: str) -> list:
        """
        Возвращает список подразделений
        :return: Список словарей подразделений
        """
        url = f"{self.__urls.iis_api_base.format(district_id)}{self.__urls.iis_api_subdivisions_list}"
        response = await self.__api_request(method="get", url=url)
        if response.status == 200:
            if response.data.get("response"):
                self.__subdivisions_list = [response.data.get("response").get("withoutParams").get("main")]
                for element in response.data.get("response").get("withoutParams").get("podr"):
                    self.__subdivisions_list.append(element)
                return self.__subdivisions_list
        # Записать в лог ошибки
        return []

    def get_subdivision_detail(self, short_name: str) -> dict:
        """

        """
        for subdivision in self.__subdivisions_list:
            if subdivision.get("naz_s") == short_name:
                return subdivision

    def get_record_preliminary(self):
        """

        """
        payload = {
            "ids": "76",
            "tipw": "2",
            "idUsl": "228",
            "dat": "30-10-2021",
            "time": "08-00",
            "fio": "Булгаков Михаил Петрович"
        }

    async def __get_subdivision_schedule(self, district_id: str, id_subdivision: str) -> dict:
        """

        :param id_subdivision:
        :return:
        """
        url = f"{self.__urls.iis_api_base.format(district_id)}{self.__urls.iis_api_schedule_list}"
        payload = {
            "ids": id_subdivision
        }
        response = await self.__api_request(method="get", url=url, params=payload)
        if response.status == 200:
            return response.data.get("response")

    async def get_subdivision_schedule(self, district_id: str, id_subdivision) -> str:
        """

        """
        subdivision_schedule = await self.__get_subdivision_schedule(district_id, id_subdivision)
        msg = []
        if subdivision_schedule:
            for element in subdivision_schedule.get("withoutParams").items():
                day_of_week, schedule = element
                abbr_day = self.__days_of_week.get(day_of_week)
                if isinstance(schedule, dict):
                    start_time = schedule.get('tim_b')[:2]
                    end_time = schedule.get('tim_e')[:2]
                    start_pause = schedule.get('br_from')[:2]
                    end_pause = schedule.get('br_to')[:2]
                    # Проверить наличие перерыва
                    if start_pause:
                        msg.append(f"{abbr_day}: с {start_time} до {end_time}; перерыв: с {start_pause} до {end_pause}")
                    # Если нет перерыва
                    else:
                        msg.append(f"{abbr_day}: {start_time}-{end_time}; без перерыва")
                elif isinstance(schedule, str):
                    msg.append(f"{abbr_day}: {schedule.lower()}")
            return "\n".join(msg)
        msg = [
            f"{self.__emojis.cross_mark} Не удалось получить расписание в подразделении",
        ]
        return "\n".join(msg)

    async def get_near_offices(self, district_id: str, lat_user: float, lon_user: float, number_nearest: int = 2) -> list:
        """

        """
        # Вычислить расстояние до каждого подразделения и добавить в словарь
        # с подразделениями данные с расстоянием и временем в пути
        near_offices_list = []
        subdivisions_list = await self.get_subdivisions_list(district_id)
        for subdivision in subdivisions_list:
            # Если координаты подразделения есть в базе данных
            if subdivision.get("map"):
                lat_subdivision = float(subdivision.get("map").get("x"))
                lon_subdivision = float(subdivision.get("map").get("y"))
                origins = (lat_user, lon_user)
                destination = (lat_subdivision, lon_subdivision)
                # Посчитать расстояние и время в пути и обновить словарь с данными подразделения
                distance = self.__gmaps.distance_matrix(origins,
                                                        destination,
                                                        mode="driving").get("rows")[0].get("elements")[0]
                subdivision.update({"distance": distance.get("distance").get("value")})
                subdivision.update({"duration": distance.get("duration").get("text")})
                near_offices_list.append(subdivision)
        # Отсортировать список словарей по ключу и вернуть
        # number_nearest первых элементов отсортированного списка
        return sorted(near_offices_list, key=itemgetter("distance"))[:number_nearest]
