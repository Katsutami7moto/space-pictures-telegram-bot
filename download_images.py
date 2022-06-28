import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image


def get_file_ext_from_url(url: str) -> str:
    return Path(urlparse(url).path).suffix


def compress_image(image_path: Path, max_image_size: int = 10000000):
    image_size = os.path.getsize(image_path)
    if image_size > max_image_size:
        image = Image.open(image_path)
        image.thumbnail((1920, 1920))
        image.save(image_path)


def download_picture(images_path: Path, pic_url: str, file_name: str,
                     params: dict = None) -> Path:
    pic_response = requests.get(pic_url, params=params)
    pic_response.raise_for_status()
    file_path = images_path.joinpath(
        f'{file_name}{get_file_ext_from_url(pic_url)}'
    )
    with open(file_path, 'wb') as file:
        file.write(pic_response.content)
    return file_path


def download_pictures_to_dir(images_path: Path, pics: list, prefix: str,
                             params: dict = None) -> list:
    now_formatted = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    downloaded_pictures = []
    for number, link in enumerate(pics):
        file_name = f'{prefix}_{now_formatted}_{number:03d}'
        downloaded_pictures.append(
            download_picture(images_path, link, file_name, params=params)
        )
    return downloaded_pictures
