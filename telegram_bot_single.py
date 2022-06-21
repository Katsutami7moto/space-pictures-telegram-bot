import argparse
import os
import random

from dotenv import load_dotenv

from telegram_bot_publish_photo import publish_photo


def get_rand_img(images_dir: str) -> str:
    images = tuple(os.walk(images_dir))[0][2]
    return os.path.join(images_dir, random.choice(images))


def main(path: str = None):
    load_dotenv()
    images_dir: str = os.getenv('IMAGES_DIR')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file',
        help='Picture to post',
        default=get_rand_img(images_dir)
    )
    args = parser.parse_args()
    if path:
        single_image_path: str = path
    else:
        single_image_path: str = args.file
    publish_photo(single_image_path)


if __name__ == "__main__":
    main()
