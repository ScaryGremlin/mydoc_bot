import sqlite3
from typing import Iterable, Any

import aiosqlite

from data import creds


class DBConnector:
    """
    Класс взаимодействия с базой данных
    """
    def __init__(self, db_file_name: str = creds.DB_FILE_NAME):
        self.__db_file_name = db_file_name

    async def __execute_query(self, text_query: str = None, params: Iterable[Any] = None) -> Iterable[sqlite3.Row]:
        """
        Выполнить SQL-запрос
        :param text_query: Текст запроса
        :param params: Итерируемый объект с перечислением параметров запроса
        :return: Результат запроса
        """
        async with aiosqlite.connect(self.__db_file_name) as db_conn:
            cursor = await db_conn.cursor()
            await cursor.execute(text_query, params)
            await db_conn.commit()
            return await cursor.fetchall()

    async def create_users_table(self) -> None:
        """
        Создать таблицу с данными пользователей в базе данных бота
        :return:
        """
        query = """CREATE TABLE IF NOT EXISTS users (
                        tg_user_id INTEGER UNIQUE NOT NULL,
                        district_id TEXT,
                        surname TEXT,
                        mobile TEXT,
                        cases JSON
                    )"""
        await self.__execute_query(query)

    async def create_districts_table(self) -> None:
        """

        """
        query = """CREATE TABLE IF NOT EXISTS districts (
                        id TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        subdivisions JSON
                    )"""
        await self.__execute_query(query)

    async def add_or_replace_user(self, tg_user_id: int,
                                  district_id: str = None,
                                  surname: str = None,
                                  mobile: str = None,
                                  cases: dict = None) -> None:
        """
        Добавить пользователя в базу данных бота.
        :param tg_user_id: ID пользователя в Telegram
        :param district_id: id района
        :param surname: Фамилия пользователя
        :param mobile: Мобильный телефон пользователя
        :param cases: Дела пользователя в формате json
        :return:
        """
        query = "INSERT OR REPLACE INTO users (tg_user_id, district_id, surname, mobile, cases) VALUES (?, ?, ?, ?, ?)"
        params = (tg_user_id, district_id, surname, mobile, cases)
        await self.__execute_query(query, params)

    async def update_user_info(self, tg_user_id: int,
                               district_id: str = None,
                               surname: str = None,
                               mobile: str = None,
                               cases: str = None) -> None:
        """

        """
        query = "UPDATE users SET"
        params = []
        if district_id:
            query += " district_id = ?,"
            params.append(district_id)
        if surname:
            query += " surname = ?,"
            params.append(surname)
        if mobile:
            query += " mobile = ?,"
            params.append(mobile)
        if cases:
            query += " cases = ?"
            params.append(cases)
        query += " WHERE tg_user_id = ?"
        params.append(tg_user_id)
        print(query)
        print(params)
        await self.__execute_query(query, params)

    async def get_user_info(self, tg_user_id: int) -> Iterable[sqlite3.Row]:
        """
        Получить информацию о пользователе из базы данных бота.
        Фамилию, мобильный теефон и дела пользователя в формате json
        :param tg_user_id: ID пользователя в Telegram
        :return: id района, фамилия, мобильный телефон и дела пользователя
        """
        query = "SELECT district_id, surname, mobile, cases FROM users WHERE tg_user_id = ?"
        params = (tg_user_id, )
        return await self.__execute_query(query, params)

    async def delete_user(self, tg_user_id: int) -> Iterable[sqlite3.Row]:
        """
        Удалить пользователя из базы данных бота
        :param tg_user_id: ID пользователя в Telegram
        :return:
        """
        query = "DELETE FROM users WHERE tg_user_id = ?"
        params = (tg_user_id, )
        return await self.__execute_query(query, params)

    async def select_all_users(self) -> Iterable[sqlite3.Row]:
        """
        Выбрать всех пользователей из базы данных бота
        :return: Кортеж с данными всех пользователей
        """
        query = "SELECT * FROM users"
        return await self.__execute_query(query)
