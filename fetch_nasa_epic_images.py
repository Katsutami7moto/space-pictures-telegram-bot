from datetime import datetime
from pathlib import Path

import requests
from environs import Env

from download_images import download_pictures_to_dir, compress_image


def get_nasa_epic_ids(api_key: str) -> list:
    api_url = 'https://api.nasa.gov/EPIC/api/natural'
    params = {
        'api_key': api_key,
    }
    api_response = requests.get(url=api_url, params=params)
    api_response.raise_for_status()
    epic_response: list = api_response.json()
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


def main():
    env = Env()
    env.read_env()
    nasa_api_key: str = env('NASA_API_KEY')
    images_dir: str = env('IMAGES_DIR', default='images')
    images_path = Path(images_dir)
    images_path.mkdir(parents=True, exist_ok=True)
    nasa_epic_params = {
        'api_key': nasa_api_key
    }
    downloaded_pictures = download_pictures_to_dir(
        images_path,
        fetch_nasa_epic_pics(nasa_api_key),
        prefix='nasa_epic',
        params=nasa_epic_params
    )
    for picture in downloaded_pictures:
        compress_image(picture)


if __name__ == "__main__":
    main()
