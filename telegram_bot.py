import telegram
from dotenv import load_dotenv
import os


if __name__ == "__main__":
    load_dotenv()
    telegram_api_token: str = os.getenv('TELEGRAM_API_TOKEN')
    telegram_channel_id: str = os.getenv('TELEGRAM_CHANNEL_ID')
    bot = telegram.Bot(token=telegram_api_token)
    print(bot.get_me())
    first_msg = 'Rock it!! round 2'
    bot.send_message(
        chat_id=telegram_channel_id,
        text=first_msg
    )
    file_name = 'images/spacex_2022-06-21-13-11-56_001.jpg'
    bot.send_photo(
        chat_id=telegram_channel_id,
        photo=open(file_name, 'rb')
    )
