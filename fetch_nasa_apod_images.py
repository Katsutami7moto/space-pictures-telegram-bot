import os

import requests
from dotenv import load_dotenv

from download_images import download_pictures_to_dir


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


if __name__ == "__main__":
    load_dotenv()
    nasa_api_key: str = os.getenv('NASA_API_KEY')
    images_dir: str = os.getenv('IMAGES_DIR', default='images')
    download_pictures_to_dir(
        images_dir,
        fetch_nasa_apod_pics(nasa_api_key, count=10),
        prefix='nasa_apod'
    )
