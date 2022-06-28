import argparse
import os
import random

from environs import Env
import telegram

from telegram_bot_publish_photo import publish_photo


def get_rand_img(dir_path: str) -> str:
    files = os.listdir(dir_path)
    return os.path.join(dir_path, random.choice(files))


def main():
    env = Env()
    env.read_env()
    images_dir: str = env('IMAGES_DIR', default='images')
    api_token: str = env('TELEGRAM_API_TOKEN')
    channel_id: str = env('TELEGRAM_CHANNEL_ID')
    bot = telegram.Bot(token=api_token)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file',
        help='Picture to post (only the name of file)',
        default=get_rand_img(images_dir)
    )
    args = parser.parse_args()
    single_image_path: str = args.file
    single_image_path = os.path.join(images_dir, single_image_path)
    publish_photo(bot, channel_id, single_image_path)


if __name__ == "__main__":
    main()
