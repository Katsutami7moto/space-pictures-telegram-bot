from pathlib import Path
from urllib.parse import urlparse, unquote_plus

import requests


def download_picture(pic_url: str, dir_name: str):
    pic_response = requests.get(pic_url)
    pic_response.raise_for_status()
    pics_dir = Path(dir_name)
    pics_dir.mkdir(parents=True, exist_ok=True)
    parsed_url = urlparse(pic_url)
    file_name = unquote_plus(Path(parsed_url.path).name)
    file_path = pics_dir.joinpath(file_name)
    with open(file_path, 'wb') as file:
        file.write(pic_response.content)


def main():
    # Download a picture
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    dir_name = 'images'
    download_picture(url, dir_name)


if __name__ == "__main__":
    main()
