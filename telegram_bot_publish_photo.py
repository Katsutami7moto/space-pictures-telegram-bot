import telegram


def publish_photo(bot: telegram.Bot, channel_id: str, image_path: str):
    with open(image_path, 'rb') as image:
        bot.send_photo(
            chat_id=channel_id,
            photo=image
        )
