import argparse
import os
import random
import time

from environs import Env
import telegram

from telegram_bot_publish_photo import publish_photo


def get_shuffled_images(dir_path: str) -> list:
    files = os.listdir(dir_path)
    random.shuffle(files)
    return files


def main():
    env = Env()
    env.read_env()
    images_dir: str = env('IMAGES_DIR', default='images')
    api_token: str = env('TELEGRAM_API_TOKEN')
    channel_id: str = env('TELEGRAM_CHANNEL_ID')
    bot = telegram.Bot(token=api_token)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--delay',
        help='Amount of hours to wait until next post',
        default=4
    )
    args = parser.parse_args()
    delay_hours: int = args.delay
    delay_seconds = delay_hours * 60 * 60
    while True:
        images = get_shuffled_images(images_dir)
        for image in images:
            publish_photo(
                bot, channel_id,
                os.path.join(images_dir, image)
            )
            time.sleep(delay_seconds)


if __name__ == "__main__":
    main()
