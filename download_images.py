import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()
nasa_api_key: str = os.getenv('NASA_API_KEY')


def get_file_ext_from_url(url: str) -> str:
    return Path(urlparse(url).path).suffix


def download_one_picture(pic_url: str, file_name: str, dir_name: str,
                         params: dict = None):
    pic_response = requests.get(pic_url, params=params)
    pic_response.raise_for_status()
    pics_dir = Path(dir_name)
    pics_dir.mkdir(parents=True, exist_ok=True)
    file_name += get_file_ext_from_url(pic_url)
    file_path = pics_dir.joinpath(file_name)
    with open(file_path, 'wb') as file:
        file.write(pic_response.content)


def download_pictures_to_dir(pics: list, prefix: str, params: dict = None):
    now_formatted = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    for number, link in enumerate(pics):
        file_name = f'{prefix}_{now_formatted}_{number:03d}'
        download_one_picture(link, file_name, dir_name='images', params=params)
