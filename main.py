from pathlib import Path
from urllib.parse import urlparse, unquote_plus

import requests
from datetime import datetime


def fetch_spacex_last_launch() -> list:
    api_url = 'https://api.spacexdata.com/v4/launches'
    api_response: dict = requests.get(url=api_url).json()
    flight: dict
    for flight in api_response:
        flickr_links: list = flight['links']['flickr']['original']
        if flickr_links:
            return flickr_links


def download_picture(pic_url: str, dir_name: str, file_name: str = ''):
    pic_response = requests.get(pic_url)
    pic_response.raise_for_status()
    pics_dir = Path(dir_name)
    pics_dir.mkdir(parents=True, exist_ok=True)
    parsed_url = urlparse(pic_url)
    parsed_pic_name = Path(parsed_url.path).name
    if file_name:
        file_name += f".{parsed_pic_name.split('.')[-1]}"
    else:
        file_name = unquote_plus(parsed_pic_name)
    file_path = pics_dir.joinpath(file_name)
    with open(file_path, 'wb') as file:
        file.write(pic_response.content)


def main():
    # Download a picture

    # url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    dir_name = 'images'

    # Get pictures from SpaceX api

    pic_links = fetch_spacex_last_launch()
    now_formatted = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    for number, link in enumerate(pic_links):
        file_name = f'spacex_{now_formatted}_{number:02d}'
        download_picture(link, dir_name, file_name)


if __name__ == "__main__":
    main()
