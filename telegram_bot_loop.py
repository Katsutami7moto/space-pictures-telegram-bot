import argparse
import os
import random
import time

from dotenv import load_dotenv

from telegram_bot_publish_photo import publish_photo


def get_shuffled_images(images_dir: str) -> list:
    images = tuple(os.walk(images_dir))[0][2]
    random.shuffle(images)
    return images


def main():
    load_dotenv()
    images_dir: str = os.getenv('IMAGES_DIR')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--delay',
        help='Amount of hours to wait until next post',
        default=4
    )
    args = parser.parse_args()
    delay_hours: int = args.delay
    delay_seconds = delay_hours * 60 * 60
    while True:
        images = get_shuffled_images(images_dir)
        for image in images:
            publish_photo(os.path.join(images_dir, image))
            time.sleep(delay_seconds)


if __name__ == "__main__":
    main()
