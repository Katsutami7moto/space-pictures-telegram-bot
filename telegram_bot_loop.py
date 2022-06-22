import argparse
import os
import random
import time

from telegram_bot_publish_photo import publish_photo, images_dir


def get_shuffled_images(dir_path: str) -> list:
    for root, dirs, files in os.walk(dir_path):
        random.shuffle(files)
        return files


def main():
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
