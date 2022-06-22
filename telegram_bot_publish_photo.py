import os

import telegram
from dotenv import load_dotenv

load_dotenv()
images_dir: str = os.getenv('IMAGES_DIR')


def publish_photo(image_path: str):
    telegram_api_token: str = os.getenv('TELEGRAM_API_TOKEN')
    telegram_channel_id: str = os.getenv('TELEGRAM_CHANNEL_ID')
    bot = telegram.Bot(token=telegram_api_token)
    bot.send_photo(
        chat_id=telegram_channel_id,
        photo=open(image_path, 'rb')
    )
