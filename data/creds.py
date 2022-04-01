from os import getenv

from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API = getenv("GOOGLE_MAPS_API")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_ID = getenv("BOT_ID")
BOT_ADMINS = getenv("BOT_ADMINS").split(",")
HTTP_AUTH_USER = getenv("HTTP_AUTH_USER")
HTTP_AUTH_PASS = getenv("HTTP_AUTH_PASS")
DB_FILE_NAME = getenv("DB_FILE_NAME")
DISTRICTS_FILE = getenv("DISTRICTS_FILE")
RECIPIENTS_EMAIL = getenv("RECIPIENTS_EMAIL").split(",")
SMTP_SERVER = getenv("SMTP_SERVER")
SMTP_PORT = getenv("SMTP_PORT")
SMTP_LOGIN = getenv("SMTP_LOGIN")
SMTP_PASS = getenv("SMTP_PASS")
