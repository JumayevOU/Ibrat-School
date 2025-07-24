import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = os.getenv("ADMINS").split(",")
IP = os.getenv("ip")

GROUP_ID = int(os.getenv("GROUP_ID"))