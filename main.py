import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def get_nasa_epic_ids(api_key: str) -> list:
    api_url = 'https://api.nasa.gov/EPIC/api/natural'
    params = {
        'api_key': api_key,
    }
    api_response = requests.get(url=api_url, params=params)
    api_response.raise_for_status()
    epic_response: dict = api_response.json()
    return [(epic['date'], epic['image']) for epic in epic_response]


def fetch_nasa_epic_pics(api_key: str) -> list:
    link_base = 'https://api.nasa.gov/EPIC/archive/natural/{}/png/{}.png'
    epic_pairs = get_nasa_epic_ids(api_key)
    epic_pics = []
    for epic in epic_pairs:
        epic_date, epic_img = epic
        epic_date = datetime.fromisoformat(epic_date).strftime('%Y/%m/%d')
        epic_link = link_base.format(epic_date, epic_img)
        epic_pics.append(epic_link)
    return epic_pics


def fetch_nasa_apod_pics(api_key: str, count: int) -> list:
    api_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': api_key,
        'count': count,
    }
    api_response = requests.get(url=api_url, params=params)
    api_response.raise_for_status()
    apod_response: dict = api_response.json()
    apods = filter(lambda x: 'hdurl' in x, apod_response)
    return [apod['hdurl'] for apod in apods]


def fetch_spacex_last_launch() -> list:
    api_url = 'https://api.spacexdata.com/v4/launches'
    api_response = requests.get(url=api_url)
    api_response.raise_for_status()
    spacex_response: dict = api_response.json()
    for flight in spacex_response:
        flickr_links: list = flight['links']['flickr']['original']
        if flickr_links:
            return flickr_links


def get_file_ext_from_url(url: str) -> str:
    return Path(urlparse(url).path).suffix


def download_one_picture(pic_url: str, dir_name: str, file_name: str,
                         params: dict = None):
    pic_response = requests.get(pic_url, params=params)
    pic_response.raise_for_status()
    pics_dir = Path(dir_name)
    pics_dir.mkdir(parents=True, exist_ok=True)
    file_name += get_file_ext_from_url(pic_url)
    file_path = pics_dir.joinpath(file_name)
    with open(file_path, 'wb') as file:
        file.write(pic_response.content)


def download_pictures_to_dir(pics: list, prefix: str, dir_name: str,
                             params: dict = None):
    now_formatted = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    for number, link in enumerate(pics):
        file_name = f'{prefix}_{now_formatted}_{number:03d}'
        download_one_picture(link, dir_name, file_name, params)


def main():
    load_dotenv()
    nasa_api_key: str = os.getenv('NASA_API_KEY')
    dir_name = 'images'

    # Get pictures from SpaceX api
    download_pictures_to_dir(
        fetch_spacex_last_launch(),
        'spacex',
        dir_name
    )

    # Get APOD pictures from NASA api
    download_pictures_to_dir(
        fetch_nasa_apod_pics(nasa_api_key, count=50),
        'nasa_apod',
        dir_name
    )

    # Get EPIC pictures from NASA
    nasa_epic_params = {
        'api_key': nasa_api_key
    }
    download_pictures_to_dir(
        fetch_nasa_epic_pics(nasa_api_key),
        'nasa_epic',
        dir_name,
        params=nasa_epic_params
    )


if __name__ == "__main__":
    main()
