import argparse
import os
import random

from telegram_bot_publish_photo import publish_photo, images_dir


def get_rand_img(dir_path: str) -> str:
    for root, dirs, files in os.walk(dir_path):
        return os.path.join(dir_path, random.choice(files))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file',
        help='Picture to post',
        default=get_rand_img(images_dir)
    )
    args = parser.parse_args()
    single_image_path: str = args.file
    publish_photo(single_image_path)


if __name__ == "__main__":
    main()
