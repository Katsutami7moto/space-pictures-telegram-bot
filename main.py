import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def fetch_nasa_apod_pics(api_key: str, count: int) -> list:
    api_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': api_key,
        'count': count,
    }
    api_response: dict = requests.get(url=api_url, params=params).json()
    apods = filter(lambda x: 'hdurl' in x, api_response)
    return [apod['hdurl'] for apod in apods]


def fetch_spacex_last_launch() -> list:
    api_url = 'https://api.spacexdata.com/v4/launches'
    api_response: dict = requests.get(url=api_url).json()
    flight: dict
    for flight in api_response:
        flickr_links: list = flight['links']['flickr']['original']
        if flickr_links:
            return flickr_links


def get_file_extension_from_url(url: str) -> str:
    return Path(urlparse(url).path).suffix


def download_one_picture(pic_url: str, dir_name: str, file_name: str):
    pic_response = requests.get(pic_url)
    pic_response.raise_for_status()
    pics_dir = Path(dir_name)
    pics_dir.mkdir(parents=True, exist_ok=True)
    file_name += get_file_extension_from_url(pic_url)
    file_path = pics_dir.joinpath(file_name)
    with open(file_path, 'wb') as file:
        file.write(pic_response.content)


def download_pictures_to_dir(pics: list, prefix: str, dir_name: str):
    now_formatted = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    for number, link in enumerate(pics):
        file_name = f'{prefix}_{now_formatted}_{number:02d}'
        download_one_picture(link, dir_name, file_name)


def main():
    load_dotenv()
    nasa_api_key = os.getenv('NASA_API_KEY')
    dir_name = 'images'

    # Get pictures from SpaceX api
    download_pictures_to_dir(
        fetch_spacex_last_launch(),
        'spacex',
        dir_name
    )

    # Get APOD pictures from NASA api
    download_pictures_to_dir(
        fetch_nasa_apod_pics(nasa_api_key, 50),
        'nasa_apod',
        dir_name
    )


if __name__ == "__main__":
    main()
