import telegram


def publish_photo(api_token: str, channel_id: str, image_path: str):
    bot = telegram.Bot(token=api_token)
    with open(image_path, 'rb') as image:
        bot.send_photo(
            chat_id=channel_id,
            photo=image
        )
