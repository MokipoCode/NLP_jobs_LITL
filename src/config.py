import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
SITE_URL = os.getenv('SITE_URL')
DATA = os.getenv('DATA')
MEDIA = os.getenv('MEDIA')