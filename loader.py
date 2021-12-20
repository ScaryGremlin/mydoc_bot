from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from googlemaps import Client

from data import creds
from data.emojis import Emoji
from data.districts import get_districts
from data.urls import Urls
from utils.db_connector import DBConnector
from utils.iis_connector import IisConnector

gmaps = Client(key=creds.GOOGLE_MAPS_API)
bot = Bot(token=creds.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())
iis_connector = IisConnector(auth_user=creds.HTTP_AUTH_USER, auth_pass=creds.HTTP_AUTH_PASS, google_api_client=gmaps)
db_connector = DBConnector(db_file_name=creds.DB_FILE_NAME)
districts = get_districts(creds.DISTRICTS_FILE)
scheduler = AsyncIOScheduler()
emojis = Emoji()
urls = Urls()
bot_id = int(creds.BOT_ID)
