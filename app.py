from aiogram import Dispatcher
from aiogram import executor

from loader import dispatcher, scheduler, db_connector
import filters, handlers
from utils.bot_commands import set_bot_commands
from utils.bot_scheduler_tasks import check_cases_statuses
from utils.notify_admins import on_startup_notify


async def on_startup(dp: Dispatcher):
    await set_bot_commands(dp)
    await on_startup_notify(dp)
    await db_connector.create_users_table()
    await db_connector.create_districts_table()
    scheduler.add_job(check_cases_statuses, trigger="interval", hours=1, args=(dispatcher, ))


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dispatcher, on_startup=on_startup)
