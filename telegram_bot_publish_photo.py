import os

import telegram
from PIL import Image
from dotenv import load_dotenv


def compress_image(image_path: str):
    max_image_size = 10000000
    image_size = os.path.getsize(image_path)
    if image_size > max_image_size:
        image = Image.open(image_path)
        image.thumbnail((1920, 1920))
        image.save(image_path)
    return open(image_path, 'rb')


def publish_photo(image_path: str):
    load_dotenv()
    telegram_api_token: str = os.getenv('TELEGRAM_API_TOKEN')
    telegram_channel_id: str = os.getenv('TELEGRAM_CHANNEL_ID')
    bot = telegram.Bot(token=telegram_api_token)
    image = compress_image(image_path)
    bot.send_photo(
        chat_id=telegram_channel_id,
        photo=image
    )
